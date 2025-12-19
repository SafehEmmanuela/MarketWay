import google.generativeai as genai
from app.core.config import settings
from langchain_google_genai import GoogleGenerativeAI

class LLMService:
    def __init__(self):
        self.model = None
        self._initialize()

    def _initialize(self):
        if settings.google_api_key:
            try:
                self.model = GoogleGenerativeAI(
                    model=settings.gemini_model,
                    google_api_key=settings.google_api_key,
                    temperature=settings.temperature,
                )
                print("LLM Service initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize LLM Service: {e}")
        else:
            print("GOOGLE_API_KEY not found. LLM Service disabled.")

    def extract_keyword(self, query: str) -> str:
        # if not self.model:
        #     return query

        try:
            prompt = f"""
            Extract the single most important product keyword from this query.
            Query: "{query}"
            Return ONLY the keyword by category. If it's already a keyword, return it as is.
            Example: "I need a shoe" -> "shoe"
            Example: "where can i get some drugs?" -> "pharmacy"
            Example: "red dress" -> "dress"
            Example: "I need a trouser" -> "dress"
            """
            
            response = self.model.invoke(prompt)
            if response:
                extracted = response.strip().lower()
                # Basic validation
                if len(extracted.split()) < 3:
                    return extracted
        except Exception as e:
            print(f"LLM extraction failed: {e}")
        
        return query

llm_service = LLMService()
# print(llm_service.model.invoke("yo"))

from google import genai
from google.genai import types
import os
from pathlib import Path

class AudioLLMService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = "gemini-2.5-flash"  # FREE model with audio support
        
    def extract_keyword_from_audio(self, audio_path: str) -> str:
        """Extract keyword from audio file"""
        try:
            # Upload audio
            audio_file_path = Path(audio_path)
            if not audio_file_path.exists():
                print(f"Audio file not found: {audio_path}")
                return ""

            # Upload audio correctly
            audio_file = self.client.files.upload(audio_file_path)
            
            prompt = """Listen to this audio carefully andxtract the single most important product keyword.
            Return ONLY the keyword in lowercase.
            Examples
            audio: "i need a shoe" -> "shoe"
            audio: "where can i get some drugs?" -> "pharmacy"
            audio: "red dress" -> "dress"
            audio: "I need a trouser" -> "dress"
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(parts=[
                        types.Part(file_data=types.FileData(file_uri=audio_file.uri)),
                        types.Part(text=prompt)
                    ])
                ]
            )
            
            # Cleanup
            self.client.files.delete(name=audio_file.name)
            
            return response.text.strip().lower()
            
        except Exception as e:
            print(f"Audio extraction failed: {e}")
            
audio_llm_service = AudioLLMService()
print(audio_llm_service.extract_keyword_from_audio("./sample.m4a"))
