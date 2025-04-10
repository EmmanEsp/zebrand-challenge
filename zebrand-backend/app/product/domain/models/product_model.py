from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.sql import func

from app.infraestructure.database import Base

class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(10), nullable=False, unique=True)
    name = Column(String(60), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    brand = Column(String(60))
    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))
