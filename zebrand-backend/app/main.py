from fastapi import FastAPI

from starlette.middleware.base import BaseHTTPMiddleware

from app.user.api.user_router import user_router
from app.product.api.product_router import product_router

from app.infraestructure.casbin_middleware import CasbinMiddleware
from app.infraestructure.logging_middleware import add_logging_middleware

from app.user.domain.exceptions.user_exception import UserException, user_exception_handler
from app.product.domain.exceptions.product_exception import ProductException, product_exception_handler
from app.domain.exceptions.service_exception import ServiceException, service_exception_handler

from app.infraestructure.logger import logger


def init():
    """Initialize the app
    - Configure FastAPI app
    - Configure app routes
    """
    _app = FastAPI(
        title="Seselik Services",
        description="Set of ecommerce services",
        version="0.1.0"
    )
    logger.info("Initialize the app")

    _app.add_exception_handler(UserException, user_exception_handler)
    _app.add_exception_handler(ProductException, product_exception_handler)
    _app.add_exception_handler(ServiceException, service_exception_handler)

    _app.add_middleware(CasbinMiddleware)
    #  _app.add_middleware(BaseHTTPMiddleware, dispatch=add_logging_middleware)
    
    _app.include_router(user_router)
    _app.include_router(product_router)

    return _app

app = init()
