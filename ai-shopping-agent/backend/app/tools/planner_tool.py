from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


class PlannerTool:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0,
        )

    def plan(
        self,
        query: str,
    ):

        prompt = f"""
You are an AI Shopping Agent.

User Query:

{query}

Return ONLY JSON.

Example:

{{
    "need_search": true,
    "need_reviews": true,
    "need_compare": true
}}
"""

        return self.llm.invoke(prompt).content