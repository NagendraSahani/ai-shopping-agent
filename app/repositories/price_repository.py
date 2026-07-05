from sqlalchemy.orm import Session

from app.models.price_history import PriceHistory


class PriceRepository:

    @staticmethod
    def save(
        db: Session,
        product_id: int,
        price: float,
    ):

        history = PriceHistory(
            product_id=product_id,
            price=price,
        )

        db.add(history)
        db.commit()

    @staticmethod
    def get_history(
        db: Session,
        product_id: int,
    ):

        return (
            db.query(PriceHistory)
            .filter(
                PriceHistory.product_id == product_id
            )
            .order_by(
                PriceHistory.created_at.desc()
            )
            .all()
        )