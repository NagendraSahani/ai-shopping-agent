import json

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


class ReviewTool:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,
    )

    @staticmethod
    def summarize(product):

        prompt = f"""
You are an AI Shopping Expert.

Analyze this product carefully.

Product:

{json.dumps(product, indent=2)}

Return ONLY valid JSON.

Format:

{{
    "pros":[
        "...",
        "...",
        "..."
    ],

    "cons":[
        "...",
        "...",
        "..."
    ],

    "verdict":"...",

    "recommended_for":"...",

    "buy_or_skip":"Buy"

}}

Do not return markdown.
Do not return explanation.
Return only JSON.
"""

        response = ReviewTool.llm.invoke(prompt)

        try:

            return json.loads(response.content)

        except Exception:

            return {
                "pros": [],
                "cons": [],
                "verdict": response.content,
                "recommended_for": "",
                "buy_or_skip": "Unknown",
            }