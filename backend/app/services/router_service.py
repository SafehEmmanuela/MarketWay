"""
Router Service for MarketWay Chat
Routes user queries to appropriate services (search or info)
"""

from typing import Dict, Literal
from langchain_google_genai import GoogleGenerativeAI
from app.core.config import settings


class RouterService:
    """
    Routes chat messages to appropriate service based on intent
    """
    
    def __init__(self):
        """Initialize the router service with Gemini model"""
        if not settings.google_api_key:
            raise ValueError("Google API key is required for Router Service")
        
        self.model = GoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,  # Lower temperature for consistent routing
        )
        
        print("Router Service initialized successfully.")
    
    def route(self, message: str) -> Dict[str, any]:
        """
        Determine the intent of user message and extract key information
        
        Args:
            message: User's chat message
        
        Returns:
            Dictionary with:
                - action: "search" or "info"
                - query: extracted search query (for search action)
                - topic: topic of inquiry (for info action)
        
        Example:
            >>> router.route("Where can I find shoes?")
            {"action": "search", "query": "shoes"}
            
            >>> router.route("Tell me about the market history")
            {"action": "info", "topic": "market history"}
        """
        if not message or not message.strip():
            return {"action": "info", "topic": "general"}
        
        try:
            prompt = f"""
                Analyze this user message and determine if they want to:
                1. SEARCH for a product/item in the market
                2. Get INFO about the market (history, general questions, etc.)

                User message: "{message}"

                Respond with ONLY a JSON object in this exact format:
                {{
                "action": "search" or "info",
                "data": "extracted keyword for search OR topic for info"
                }}

                Examples:
                - "Where can I find shoes?" -> {{"action": "search", "data": "shoes"}}
                - "I need pharmacy" -> {{"action": "search", "data": "pharmacy"}}
                - "Tell me about this market" -> {{"action": "info", "data": "market history"}}
                - "What is MarketWay?" -> {{"action": "info", "data": "general info"}}

                Rules:
                - If asking WHERE/FIND/NEED/LOOKING FOR a product -> "search"
                - If asking ABOUT/HISTORY/WHAT IS the market -> "info"
                - Extract only the key product name for search
                - Extract the topic for info queries

                Response:
            """
            
            response = self.model.invoke(prompt)
            result = self._parse_response(response, message)
            
            return {**result, "original_message": message}
            
        except Exception as e:
            print(f"Error routing message: {e}")
            # Default to search if unsure
            return {"action": "search", "query": message}
    
    def _parse_response(self, response: str, original_message: str) -> Dict[str, any]:
        """
        Parse LLM response into structured format
        
        Args:
            response: Raw LLM response
            original_message: Original user message (fallback)
        
        Returns:
            Structured routing dictionary
        """
        import json
        import re
        
        try:
            # Clean response (remove markdown code blocks if present)
            cleaned = response.strip()
            cleaned = re.sub(r'```json\s*|\s*```', '', cleaned)
            
            # Parse JSON
            parsed = json.loads(cleaned)
            
            action = parsed.get("action", "search")
            data = parsed.get("data", original_message)
            
            # Structure based on action
            if action == "search":
                return {
                    "action": "search",
                    "query": data
                }
            else:
                return {
                    "action": "info",
                    "topic": data
                }
                
        except Exception as e:
            print(f"Error parsing router response: {e}")
            print(f"Raw response: {response}")
            # Fallback: assume search
            return {"action": "search", "query": original_message}


# Global instance
router_service = RouterService()