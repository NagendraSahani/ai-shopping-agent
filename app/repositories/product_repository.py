from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    @staticmethod
    def save(
        db: Session,
        product: dict,
    ):

        db_product = Product(
            name=product["name"],
            platform=product["platform"],
            price=product["price"],
            rating=product["rating"],
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product