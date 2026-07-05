from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.session import get_db
from app.repositories.price_repository import PriceRepository


from app.schemas.product import (
    ProductSearchRequest,
)

from app.services.shopping_service import (
    ShoppingService,
)

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)


@router.post("/search")
def search_product(
    request: ProductSearchRequest,
):

    return ShoppingService.search(
        request.query
    )



@router.get(
    "/history/{product_id}",
)
def product_history(
    product_id: int,
    db: Session = Depends(get_db),
):

    return PriceRepository.get_history(
        db,
        product_id,
    )