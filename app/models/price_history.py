from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class PriceHistory(Base):

    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )