from fastapi import Request
from app.infraestructure.logger import logger


async def add_logging_middleware(request: Request, call_next):

    logger.info({
        "method": request.method,
        "url": request.url.path
    })

    response = await call_next(request)
    return response
