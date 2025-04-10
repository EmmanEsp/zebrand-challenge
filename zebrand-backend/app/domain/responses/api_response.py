from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    
    service_status: str
    status_code: int
    data: T
