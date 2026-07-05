import re


class ExtractorTool:

    @staticmethod
    def extract(serpapi_result: dict):

        products = []

        for item in serpapi_result.get("shopping_results", []):

            price = item.get("price", "0")

            price = re.sub(r"[^\d.]", "", price)

            try:
                price = float(price)
            except:
                price = 0.0

            products.append(
                {
                    "name": item.get("title", ""),
                    "platform": item.get("source", ""),
                    "price": price,
                    "rating": item.get("rating", 0),
                    "reviews": item.get("reviews", 0),
                    "link": (
                        item.get("product_link")
                        or item.get("link")
                        or item.get("serpapi_link")
                        or ""
                    ),

                    "thumbnail": item.get("thumbnail", ""),
                }
            )

        return products