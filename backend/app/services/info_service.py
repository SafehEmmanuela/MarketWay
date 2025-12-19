from tavily import TavilyClient
from app.core.config import settings

class InfoService:
    def __init__(self):
        self.client = None
        if settings.TAVILY_API_KEY:
            try:
                self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            except Exception as e:
                print(f"Error initializing Tavily client: {e}")

    def search(self, query: str) -> str:
        if not self.client:
            return "Online search is unavailable (API Key missing or invalid)."
        
        try:
            # Perform a search optimized for answers
            response = self.client.search(query=query, search_depth="basic", include_answer=True)
            return response.get("answer", response.get("results", "No results found."))
        except Exception as e:
            return f"Error performing online search: {str(e)}"

info_service = InfoService()
print(info_service.search("how old is the bamenda main market?"))
