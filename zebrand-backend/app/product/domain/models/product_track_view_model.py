from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.infraestructure.database import Base


class ProductTrackViewModel(Base):
    __tablename__ = 'product_track_views'
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(10))
    keyword = Column(String(100))
    viewed_at = Column(DateTime(timezone=True), default=datetime.now)
