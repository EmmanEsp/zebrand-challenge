from fastapi import APIRouter, Depends, status, BackgroundTasks

from app.domain.responses.api_response import APIResponse
from app.domain.enums import api_status
from app.product.domain.requests.product_request import ProductRequest, UpdateProductRequest, ProductFilterParams
from app.product.domain.responses.product_response import GetProductResponse, ProductResponse
from app.product.use_cases.product_use_case import ProductUseCase


product_v1_router = APIRouter()


@product_v1_router.get(
    "",
    response_model=APIResponse[GetProductResponse],
    status_code=status.HTTP_200_OK
)
def get_all_products(
    background_tasks: BackgroundTasks,
    filters: ProductFilterParams = Depends(),
    use_case: ProductUseCase = Depends()
) -> APIResponse[GetProductResponse]:
    response = use_case.get_all_products(filters)
    background_tasks.add_task(use_case.track_product_visit, response.products, filters.keyword)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=response
    )


@product_v1_router.get(
    "/sku/{sku}",
    response_model=APIResponse[ProductResponse],
    status_code=status.HTTP_200_OK
)
def get_product_by_sku(
    sku: str,
    background_tasks: BackgroundTasks,
    use_case: ProductUseCase = Depends()
) -> APIResponse[ProductResponse]:
    response = use_case.get_product_by_sku(sku)
    background_tasks.add_task(use_case.track_one_product_visit, response, sku)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=response
    )


@product_v1_router.post(
    "",
    response_model=APIResponse[None],
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductRequest, use_case: ProductUseCase = Depends()) -> APIResponse[None]:
    use_case.create_product(product)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_201_CREATED,
        data=None
    )


@product_v1_router.patch(
    "/{sku}",
    response_model=APIResponse[None],
    status_code=status.HTTP_200_OK
)
def update_product_by_sku(
    sku: str, 
    product: UpdateProductRequest, 
    use_case: ProductUseCase = Depends()
) -> APIResponse[None]:
    print(product)
    use_case.update_product(sku, product)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=None
    )


@product_v1_router.delete(
    "/{sku}",
    response_model=APIResponse[None],
    status_code=status.HTTP_200_OK
)
def delete_product_by_sku(sku: str, use_case: ProductUseCase = Depends()) -> APIResponse[None]:
    use_case.delete_product(sku)
    return APIResponse(
        service_status=api_status.SUCCESS,
        status_code=status.HTTP_200_OK,
        data=None
    )
