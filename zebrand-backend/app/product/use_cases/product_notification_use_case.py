from datetime import datetime

from fastapi import Depends, Request
from fastapi.security import HTTPBearer

from jose import jwt

from jinja2 import Template

from app.product.services.product_service import ProductService
from app.product.domain.responses.product_response import ProductChanged
from app.product.domain.templates.product_change_template import product_update_template

from app.domain.settings.security_settings import get_security_setting
from app.domain.settings.aws_settings import get_ses_client
from app.infraestructure.logger import logger


class ProductNotificationUseCase:
    
    def __init__(self, service: ProductService = Depends()) -> None:
        self._service = service

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

    async def send_update_product_notification(self, request: Request, product_changes: ProductChanged):
        logger.info("Start email notification process for product update.")
        logger.info(request)
        logger.info(product_changes)
        
        author = await self.get_author_from_request(request)
        emails = self.get_admin_email_list()
        
        changes = [change.model_dump() for change in product_changes.changes]
        datenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        template = Template(product_update_template)

        client = get_ses_client()

        html_content = template.render(
            sku=product_changes.sku,
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
        logger.info("Ended notification process")
        logger.info(response)
