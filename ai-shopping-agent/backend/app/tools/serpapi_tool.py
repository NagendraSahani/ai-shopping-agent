from serpapi import GoogleSearch

from app.core.config import settings


class SerpAPITool:

    def search(
        self,
        query: str,
    ):

        params = {
            "engine": "google_shopping",
            "q": query,
            "gl": "in",
            "hl": "en",
            "api_key": settings.SERPAPI_API_KEY,
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        return results