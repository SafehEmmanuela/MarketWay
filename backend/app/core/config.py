import os
from dotenv import load_dotenv

class Settings:
    PROJECT_NAME: str = "MarketWay Navigator API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Base path for data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Load .env explicitly
    load_dotenv(os.path.join(BASE_DIR, ".env"))

    DATA_DIR = os.path.join(BASE_DIR, "data")
    IMAGES_DIR = os.path.join(DATA_DIR, "images")
    JSON_PATH = os.path.join(DATA_DIR, "marketway.json")
    PDF_PATH = os.path.join(DATA_DIR, "Bamenda_Main_Market_History.pdf")
    
    # External APIs
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    google_api_key = os.getenv("GOOGLE_API_KEY", "")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    temperature = os.getenv("TEMPERATURE")

settings = Settings()
