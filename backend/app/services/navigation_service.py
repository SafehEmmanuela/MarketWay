"""
Navigation Service for MarketWay
Converts technical directions into human-friendly navigation instructions
"""

from typing import Dict
from langchain_google_genai import GoogleGenerativeAI
from app.core.config import settings


class NavigationService:
    """
    Service to convert line data into human-friendly navigation directions
    using Google Generative AI
    """
    
    def __init__(self):
        """Initialize the navigation service with Gemini model"""
        if not settings.google_api_key:
            raise ValueError("Google API key is required for Navigation Service")
        
        self.model = GoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.6,
        )
        
        print("Navigation Service initialized successfully.")
    
    def navigate(self, line_data: Dict) -> str:
        """
        Generate human-friendly navigation directions to a line
        
        Args:
            line_data: Dictionary containing line information with keys:
                - line_name: str (e.g., "godly line")
                - direction: str (e.g., "Aisle 1, Position 2 (near the beginning of aisle 1)")
        
        Returns:
            Human-friendly navigation instructions as a string
        """
        if not line_data:
            return "No line data provided for navigation."
        
        line_name = line_data.get("line_name", "the line")
        direction = line_data.get("direction", "")
        interest = line_data.get("matched_term", "products")
        
        if not direction:
            return f"Direction information not available for '{line_name}'."
        
        try:
            prompt = f"""
                You are a friendly market guide helping customers navigate MarketWay market.

                Convert this technical direction into warm, conversational and brief easy-to-follow navigation instructions:

                Line Name: "{line_name}"
                Technical Direction: {direction}
                I need you to understand that all the directions you provide are from the main entrance to the market.
                When entering through the main gate, you get straight into aisle 1 which is long with lines on the right.
                To get to aisle 2, after entering the main gate, you turn left directly on the first line you see. A right turn a few metres ahead from this line entrance leads to aisle 2 which has lines on the left.
                This {direction} is interms of aisle and order. I have explained how to provide aisle directions, the order simply represents the line position.
                Order of one means on the specific aisle, the line is the first you meet on your right/left depending on the aisle
                
                Examples
                1. direction: "Aisle 1, Position 2 (near the beginning of aisle 1)
                your response: "Enter through the main gate and walk straight down the aisle you see. The second line on your RIGHT is {line_name}, where you can find stalls selling {interest}"
                
                2.direction: "Aisle 2, Position 3 
                your response: "Enter through the main gate and make the first left turn. Walk straight ahead until you make a right turn into aisle2. The second line on your LEFT is {line_name}, where you can find stalls selling {interest}"

                Instructions:
                1. Make the directions conversational and friendly
                2. Be specific about directions
                3. Keep it concise (2-3 sentences max)
                4. Mention the line name naturally
                5. Include what products can be found there
                Use the examples i've provided as a guide. YOu can summarize and make your response more concise

                Please do not say "to find <line name>" in your response. The user is only interested in what he/she wants so
                lay more emphasis on the users' interest. Please make sure you mention the product in your response. like toward the end you can say where you will find <interest>. Not necessarily exacly like this, but you get the vibe.
                
                DO NOT EMPHASIZE THE LINE NAME MORE THAN THE PRODUCT OF INTEREST. THE USER IS MORE INTERESTED IN FINDING HIS/HER PRODUCT THAN THE LINE NAME.
                Say something like "the second line you see on your right is **godly line**, where you can find stalls selling {interest}".
                Generate friendly directions:
            """
            
            response = self.model.invoke(prompt)
            return response.strip()
            
        except Exception as e:
            print(f"Error generating navigation directions: {e}")
            return f"You can find '{line_name}' at: {direction}"


# Global instance
navigation_service = NavigationService()

# print(navigation_service.navigate({
#       "line_id": "l2",
#       "line_name": "godly line",
#       "aisle": 1,
#       "items_sold": [
#         "shoes",
#         "dresses",
#         "roomdecoitems",
#         "bags",
#         "babystuff"
#       ],
#       "order": 2,
#       "match_type": "item",
#       "matched_term": "shoes",
#       "direction": "Aisle 1, Position 2 (near the beginning of aisle 1)"
#     }))