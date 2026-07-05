from difflib import SequenceMatcher


class CompareTool:

    TRUSTED_PLATFORMS = {
        "Amazon": 1.00,
        "Amazon.in": 1.00,
        "Flipkart": 0.98,
        "Croma": 0.95,
        "Reliance Digital": 0.95,
        "Vijay Sales": 0.93,
    }

    @staticmethod
    def remove_duplicates(products):

        unique = []

        for product in products:

            duplicate = False

            for existing in unique:

                similarity = SequenceMatcher(
                    None,
                    product.get("name", "").lower(),
                    existing.get("name", "").lower(),
                ).ratio()

                if similarity > 0.90:
                    duplicate = True
                    break

            if not duplicate:
                unique.append(product)

        return unique

    @staticmethod
    def normalize(value, minimum, maximum):

        if maximum == minimum:
            return 1

        return (value - minimum) / (maximum - minimum)

    @staticmethod
    def compare(products):

        if not products:
            return None

        products = CompareTool.remove_duplicates(products)

        prices = [
            float(p.get("price", 0))
            for p in products
            if p.get("price", 0) > 0
        ]

        ratings = [
            float(p.get("rating", 0))
            for p in products
        ]

        reviews = [
            int(p.get("reviews", 0))
            for p in products
        ]

        min_price = min(prices)
        max_price = max(prices)

        min_rating = min(ratings)
        max_rating = max(ratings)

        min_reviews = min(reviews)
        max_reviews = max(reviews)

        for p in products:

            price = float(p.get("price", 0))
            rating = float(p.get("rating", 0))
            review_count = int(p.get("reviews", 0))
            platform = p.get("platform", "")
            discount = float(p.get("discount", 0))
            availability = int(
                p.get("availability", 1)
            )

            # lower price = higher score
            if max_price == min_price:
                price_score = 1
            else:
                price_score = (
                    max_price - price
                ) / (
                    max_price - min_price
                )

            rating_score = CompareTool.normalize(
                rating,
                min_rating,
                max_rating,
            )

            review_score = CompareTool.normalize(
                review_count,
                min_reviews,
                max_reviews,
            )

            seller_score = CompareTool.TRUSTED_PLATFORMS.get(
                platform,
                0.60,
            )

            discount_score = min(
                discount / 100,
                1,
            )

            availability_score = availability

            total = (

                price_score * 25

                +

                rating_score * 30

                +

                review_score * 25

                +

                seller_score * 10

                +

                availability_score * 5

                +

                discount_score * 5

            )

            p["comparison"] = {

                "price_score": round(
                    price_score * 25,
                    2,
                ),

                "rating_score": round(
                    rating_score * 30,
                    2,
                ),

                "review_score": round(
                    review_score * 25,
                    2,
                ),

                "seller_score": round(
                    seller_score * 10,
                    2,
                ),

                "availability_score": round(
                    availability_score * 5,
                    2,
                ),

                "discount_score": round(
                    discount_score * 5,
                    2,
                ),

                "total_score": round(
                    total,
                    2,
                ),

            }

            p["confidence"] = min(
                100,
                round(total),
            )

        best = max(
            products,
            key=lambda x: x["comparison"]["total_score"],
        )

        return best