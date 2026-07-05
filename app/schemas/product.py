from pydantic import BaseModel


class ProductSearchRequest(BaseModel):
    query: str


class ProductResponse(BaseModel):

    name: str

    platform: str

    price: float

    rating: float

    url: str