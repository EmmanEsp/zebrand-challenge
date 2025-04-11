from decimal import Decimal

from pydantic import BaseModel


class PaginationMetadata(BaseModel):

    page: int
    size: int
    total_size: int
    total_pages: int


class ProductResponse(BaseModel):
    
    sku: str
    name: str
    price: Decimal
    brand: str


class GetProductResponse(BaseModel):

    products: list[ProductResponse]
    metadata: PaginationMetadata


class ProductChanges(BaseModel):
    
    field: str
    old: str
    new: str
