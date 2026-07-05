from sqlalchemy.orm import Session

from app.models.price_history import PriceHistory


class HistoryTool:

    @staticmethod
    def history(
        db: Session,
        product_id: int,
    ):

        return (
            db.query(PriceHistory)
            .filter(
                PriceHistory.product_id == product_id
            )
            .all()
        )