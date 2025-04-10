import math
from datetime import datetime
from fastapi import Depends, status

from app.product.services.product_service import ProductService
from app.product.domain.responses.product_response import ProductResponse, GetProductResponse, PaginationMetadata
from app.product.domain.requests.product_request import ProductRequest, UpdateProductRequest, ProductFilterParams
from app.product.domain.models.product_model import ProductModel
from app.product.domain.models.product_track_view_model import ProductTrackViewModel
from app.product.domain.exceptions.product_exception import ProductException


class ProductUseCase:
    
    def __init__(self, service: ProductService = Depends()) -> None:
        self._service = service

    def get_all_products(self, filters: ProductFilterParams) -> GetProductResponse:
        query = self._service.get_active_products_query()
        if filters.keyword:
            query = self._service.get_query_by_keyword(filters.keyword)
        
        total_size = query.count()
        total_pages = math.ceil(total_size / filters.size) if filters.size > 0 else 1

        pagination = PaginationMetadata(
            page=filters.page,
            size=filters.size,
            total_size=total_size,
            total_pages=total_pages
        )
        
        products = self._service.get_all_product_from_query(filters, query)

        product_response = [
            ProductResponse(
                sku=product.sku,
                name=product.name,
                price=product.price,
                brand=product.brand
            )
            for product in products
        ]

        print("PRODUCTS", product_response)

        response = GetProductResponse(
            metadata=pagination,
            products=product_response
        )

        return response

    def get_product_by_sku(self, sku: str) -> ProductResponse:
        product = self._service.get_product_by_sku(sku)
        if product is None:
            raise ProductException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"sku": f"Product with SKU: {sku} not found."}
            )
        response = ProductResponse(
            brand=product.brand,
            name=product.name,
            price=product.price,
            sku=product.sku
        )
        return response
        

    def create_product(self, product: ProductRequest) -> None:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price,
            brand=product.brand
        )
        self._service.save_product(new_product)
    
    def update_product(self, sku: str, values: UpdateProductRequest) -> None:
        product = self._service.get_product_by_sku(sku)
        if product is None:
            raise ProductException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"sku": "Product not found."}
            )
        
        update_data = values.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(product, field):
                setattr(product, field, value)
        self._service.save_product(product)
    
    def delete_product(self, sku: str) -> None:
        product = self._service.get_product_by_sku(sku)
        if product is None:
            raise ProductException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"sku": "Product not found."}
            )
        product.is_deleted = True
        product.deleted_at = datetime.now()
        self._service.save_product(product)

    def track_product_visit(self, products: list[ProductResponse], keyword: str) -> None:
        tracked_products = [
            ProductTrackViewModel(
                sku=product.sku,
                keyword=keyword
            )
            for product in products
        ]
        if len(tracked_products) > 0:
            self._service.bulk_save_product_visited(tracked_products)

    def track_one_product_visit(self, product: ProductResponse, keyword: str) -> None:
        tracked_product = ProductTrackViewModel(sku=product.sku, keyword=keyword)
        self._service.save_product_visited(tracked_product)
