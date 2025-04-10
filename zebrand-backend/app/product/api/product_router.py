from fastapi import APIRouter

from app.product.api.v1.product_controller import product_v1_router


product_router = APIRouter()

product_router.include_router(
    product_v1_router,
    prefix="/api/v1/product",
    tags=["Product"]
)
