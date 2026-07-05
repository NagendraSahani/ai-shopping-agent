import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
)


prompt = ChatPromptTemplate.from_template("""
You are an AI Shopping Expert.

User Query:
{query}

Products:
{products}

Compare all products and return ONLY valid JSON.

{{
    "best_platform": "",
    "best_price": "",
    "best_rating": "",
    "recommendation": "",
    "pros": [],
    "cons": []
}}

Do not use markdown.
Return JSON only.
""")


class AIService:

    @staticmethod
    def analyze(query, products):

        chain = prompt | llm

        response = chain.invoke(
            {
                "query": query,
                "products": json.dumps(products, indent=2),
            }
        )

        
        return json.loads(response.content)