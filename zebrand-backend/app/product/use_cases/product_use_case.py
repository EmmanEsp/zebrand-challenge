import math
from datetime import datetime
from pathlib import Path

from fastapi import Depends, status, Request
from fastapi.security import HTTPBearer

from jose import jwt

from jinja2 import Template
import boto3

from app.product.services.product_service import ProductService
from app.product.domain.responses.product_response import ProductResponse, GetProductResponse, PaginationMetadata, ProductChanges
from app.product.domain.requests.product_request import ProductRequest, UpdateProductRequest, ProductFilterParams
from app.product.domain.models.product_model import ProductModel
from app.product.domain.models.product_track_view_model import ProductTrackViewModel
from app.product.domain.exceptions.product_exception import ProductException
from app.domain.settings.security_settings import get_security_setting
from app.domain.settings.aws_settings import get_ses_client


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
    
    def update_product(self, sku: str, values: UpdateProductRequest) -> list[ProductChanges]:
        product = self._service.get_product_by_sku(sku)
        if product is None:
            raise ProductException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"sku": "Product not found."}
            )
        
        update_data = values.model_dump(exclude_unset=True)
        changes = []
        for field, value in update_data.items():
            if hasattr(product, field):
                changes.append(ProductChanges(
                    field=field,
                    old=str(getattr(product, field)),
                    new=str(value)
                ))
                setattr(product, field, value)
        self._service.save_product(product)
        return changes
    
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

    async def get_author_from_request(self, request: Request):
        security = HTTPBearer(auto_error=False)
        credentials = await security(request)
            
        security_settings = get_security_setting()

        payload = jwt.decode(
            credentials.credentials,
            security_settings.secret_key,
            algorithms=[security_settings.algorithm]
        )

        author = payload["sub"]
        return author
    
    def get_admin_email_list(self) -> list[str]:
        admins = self._service.get_all_admin_user()
        emails = [admin.email for admin in admins]
        return emails

    async def send_product_change_email(self, request: Request, product_changes: list[ProductChanges]):
        author = await self.get_author_from_request(request)
        emails = self.get_admin_email_list()
        
        changes = [change.model_dump() for change in product_changes]
        datenow = datetime.now()

        path = Path(__file__).parent.parent
        template_path = str(path / "domain" / "templates" / "product_change_template.html")
        template = Template(template_path)

        client = get_ses_client()

        html_content = template.render(
            author=author,
            changes=changes,
            current_date=datenow
        )
        response = client.send_email(
            Destination={
                'ToAddresses': emails,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': html_content,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': "Product Update Notification",
                },
            },
            Source=author,
        )
        print(response)
