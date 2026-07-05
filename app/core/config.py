from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GOOGLE_API_KEY: str

    DATABASE_URL: str

    SECRET_KEY: str

    TAVILY_API_KEY: str

    SERPAPI_API_KEY: str

    ALGORITHM: str = "HS256"

    API_PREFIX: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    PROJECT_NAME: str = "AI Shopping Agent"

    VERSION: str = "1.0"

    class Config:
        env_file = ".env"


settings = Settings()