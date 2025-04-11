from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from decimal import Decimal


class ProductRequest(BaseModel):

    sku: Annotated[str, Field(max_length=10, min_length=4)]
    name: Annotated[str, Field(max_length=60, min_length=4)]
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)]
    brand: Annotated[str, Field(max_length=60)]


class UpdateProductRequest(BaseModel):

    sku: Annotated[str, Field(max_length=10, min_length=4)] = None
    name: Annotated[str, Field(max_length=60, min_length=4)] = None
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2, gt=0)] = None
    brand: Annotated[str, Field(max_length=60)] = None


class ProductFilterParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    keyword: Optional[str] = Field(None)

    model_config = ConfigDict(validate_by_name=True)
