from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.user.api.user_router import user_router
from app.product.api.product_router import product_router

from app.infraestructure.casbin_middleware import CasbinMiddleware

from app.user.domain.exceptions.user_exception import UserException, user_exception_handler
from app.product.domain.exceptions.product_exception import ProductException, product_exception_handler
from app.domain.exceptions.service_exception import ServiceException, service_exception_handler


def init():
    """Initialize the app
    - Configure FastAPI app
    - Configure app routes
    """
    _app = FastAPI(
        title="Zebrand Services",
        description="Set of ecommerce services",
        version="0.1.0"
    )

    _app.add_exception_handler(UserException, user_exception_handler)
    _app.add_exception_handler(ProductException, product_exception_handler)
    _app.add_exception_handler(ServiceException, service_exception_handler)

    _app.add_middleware(CasbinMiddleware)
    
    _app.include_router(user_router)
    _app.include_router(product_router)

    def custom_openapi():
        if _app.openapi_schema:
            return _app.openapi_schema
        openapi_schema = get_openapi(
            title=_app.title,
            version=_app.version,
            description=_app.description,
            routes=_app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", [{"BearerAuth": []}])
        _app.openapi_schema = openapi_schema
        return _app.openapi_schema

    _app.openapi = custom_openapi

    return _app

app = init()
