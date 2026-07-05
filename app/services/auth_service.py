from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, LoginRequest
from app.core.security import (
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user: UserCreate,
    ):

        existing_user = UserRepository.get_by_email(
            db,
            user.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

        return UserRepository.create(
            db,
            user,
        )

    @staticmethod
    def login(
        db: Session,
        user: LoginRequest,
    ):

        db_user = UserRepository.login(
            db,
            user.email,
        )

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        if not verify_password(
            user.password,
            db_user.password,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {
                "sub": db_user.email,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }