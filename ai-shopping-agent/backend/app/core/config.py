from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GOOGLE_API_KEY: str

    TAVILY_API_KEY: str

    SERPAPI_API_KEY: str

    PROJECT_NAME: str = "AI Shopping Agent"

    VERSION: str = "1.0"

    class Config:
        env_file = ".env"


settings = Settings()
