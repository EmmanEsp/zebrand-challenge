from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session, Query

from app.infraestructure.database import get_db
from app.product.domain.requests.product_request import ProductFilterParams
from app.product.domain.models.product_model import ProductModel
from app.product.domain.models.product_track_view_model import ProductTrackViewModel
from app.user.domain.models.user_model import UserModel


class ProductService:
    
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self._db = db
    
    def get_active_products_query(self) -> Query[ProductModel]:
        return self._db.query(ProductModel).filter(ProductModel.is_deleted == False)

    def get_all_admin_user(self) -> list[UserModel]:
        return self._db.query(UserModel).filter(UserModel.is_deleted == False, UserModel.role == "admin").all()

    def get_product_by_sku(self, sku: str) -> ProductModel:
        return self.get_active_products_query().filter(ProductModel.sku == sku).first()

    def get_query_by_keyword(self, keyword: str) -> Query[ProductModel]:
        search = f"%{keyword}%"
        query = self.get_active_products_query().filter(
            or_(
                ProductModel.sku.ilike(search),
                ProductModel.name.ilike(search),
                ProductModel.brand.ilike(search)
            )
        )
        return query
    
    def get_all_product_from_query(self, filters: ProductFilterParams, query: Query[ProductModel]):
        return query.offset((filters.page - 1) * filters.size).limit(filters.size).all()

    def get_product_by_id(self, product_id: int) -> ProductModel | None:
        return self.get_active_products_query().filter(ProductModel.id == product_id).first()

    def get_all_products(self) -> list[ProductModel]:
        return self.get_active_products_query().all()
    
    def save_product(self, product: ProductModel) -> None:
        self._db.add(product)
        self._db.commit()
    
    def bulk_save_product_visited(self, tracked_products: list[ProductTrackViewModel]) -> None:
        self._db.bulk_save_objects(tracked_products)
        self._db.commit()
    
    def save_product_visited(self, tracked_product: ProductTrackViewModel) -> None:
        self._db.add(tracked_product)
        self._db.commit()
