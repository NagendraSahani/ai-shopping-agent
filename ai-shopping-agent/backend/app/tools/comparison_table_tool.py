class ComparisonTableTool:

    @staticmethod
    def build(products):

        table = []

        for p in products:

            comparison = p.get(
                "comparison",
                {},
            )

            table.append({

                "rank": 0,

                "name": p.get(
                    "name",
                    "",
                ),

                "platform": p.get(
                    "platform",
                    "",
                ),

                "price": p.get(
                    "price",
                    0,
                ),

                "rating": p.get(
                    "rating",
                    0,
                ),

                "reviews": p.get(
                    "reviews",
                    0,
                ),

                "confidence": p.get(
                    "confidence",
                    0,
                ),

                "score": comparison.get(
                    "total_score",
                    0,
                ),

                "buy_link": p.get(
                    "link",
                    "",
                ),

                "thumbnail": p.get(
                    "thumbnail",
                    "",
                ),

                "winner": False,

            })

        table.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        for i, product in enumerate(table):

            product["rank"] = i + 1

            if i == 0:

                product["winner"] = True

        return table