import json

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


class RecommendationTool:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.2,
    )

    @staticmethod
    def recommend(
        best_product,
        all_products,
    ):

        prompt = f"""
You are an expert AI Shopping Assistant.

Analyze the following products and recommend the best one.

Best Product:

{best_product}

All Products:

{all_products}

Return ONLY valid JSON.

{{
    "decision":"BUY / CONSIDER / SKIP",

    "summary":"",

    "winner_reason":"",

    "pros":[
        "",
        "",
        ""
    ],

    "cons":[
        "",
        ""
    ],

    "best_for":[
        "",
        "",
        ""
    ],

    "avoid_if":[
        "",
        ""
    ],

    "value_for_money":"Excellent / Good / Average / Poor"
}}
"""

        response = RecommendationTool.llm.invoke(
            prompt
        ).content

        try:

            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(response)

        except Exception:

            return {

                "decision": "UNKNOWN",

                "summary": response,

                "winner_reason": "",

                "pros": [],

                "cons": [],

                "best_for": [],

                "avoid_if": [],

                "value_for_money": "Unknown",

            }