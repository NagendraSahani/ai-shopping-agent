from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


class ReviewTool:

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,
    )

    @staticmethod
    def summarize(products):

        prompt = f"""
Analyze these products.

{products}

Return:

- strengths
- weaknesses
- buying recommendation
"""

        return ReviewTool.llm.invoke(prompt).content