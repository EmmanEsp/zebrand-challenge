from pydantic import BaseModel, Field
from typing import Annotated, Optional
from decimal import Decimal


class ProductRequest(BaseModel):

    sku: Annotated[str, Field(max_length=10, min_length=4)]
    name: Annotated[str, Field(max_length=60, min_length=4)]
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)]
    brand: Annotated[str, Field(max_length=60)]


class UpdateProductRequest(BaseModel):

    sku: Optional[Annotated[str, Field(max_length=10, min_length=4)]]
    name: Optional[Annotated[str, Field(max_length=60, min_length=4)]]
    price: Optional[Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)]]
    brand: Optional[Annotated[str, Field(max_length=60)]]


class ProductFilterParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    keyword: Optional[str] = Field(None)

    class Config:
        validate_by_name = True
