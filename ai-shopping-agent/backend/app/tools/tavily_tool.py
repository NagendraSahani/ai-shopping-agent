from tavily import TavilyClient

from app.core.config import settings


class TavilyTool:

    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(
        self,
        query: str,
    ):

        response = self.client.search(
            query=query,
            max_results=5,
        )

        return response