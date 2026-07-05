from app.services.ai_service import AIService
from app.database.session import SessionLocal

from app.repositories.product_repository import ProductRepository
from app.repositories.price_repository import PriceRepository


class ShoppingService:

    @staticmethod
    def search(query: str):

        products = [

            {
                "platform": "Amazon",
                "name": "ASUS Vivobook 15",
                "price": 54999,
                "rating": 4.4,
            },

            {
                "platform": "Flipkart",
                "name": "ASUS Vivobook 15",
                "price": 53999,
                "rating": 4.5,
            },

            {
                "platform": "Croma",
                "name": "ASUS Vivobook 15",
                "price": 54899,
                "rating": 4.3,
            },

        ]

        db = SessionLocal()

        try:

            for product in products:

                # Product save
                saved = ProductRepository.save(
                    db,
                    product,
                )

                # Price history save
                PriceRepository.save(
                    db,
                    saved.id,
                    saved.price,
                )

        finally:
            db.close()

        # AI Analysis
        ai_result = AIService.analyze(
            query=query,
            products=products,
        )

        return {
            "query": query,
            "products": products,
            "analysis": ai_result,
        }