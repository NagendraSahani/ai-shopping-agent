class CompareTool:

    @staticmethod
    def compare(products):

        if len(products) == 0:
            return None

        best = sorted(
            products,
            key=lambda x: (
                -float(x.get("rating", 0)),
                float(x.get("price", 9999999)),
            ),
        )[0]

        return best