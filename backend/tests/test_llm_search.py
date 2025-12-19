import sys
import os
from unittest.mock import MagicMock, patch

# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

# Mock settings before importing services that use it
settings.GEMINI_API_KEY = "dummy_key"

def test_llm_service():
    print("Testing LLM Service Refactor...")

    # Patch genai where it is imported in llm_service
    with patch('google.generativeai.GenerativeModel') as MockModel:
        # We need to ensure llm_service is imported AFTER patching if we want to catch initialization
        # Or we can just test the method if it's already initialized.
        # Since we can't easily un-import, let's just patch the model instance on the service if it exists,
        # or patch the class so new instances get the mock.
        
        from app.services.llm_service import llm_service
        
        # Inject mock model manually to avoid initialization issues during test
        mock_model_instance = MockModel.return_value
        llm_service.model = mock_model_instance
        
        # Test Case 1: Extraction
        print("\n--- Test Case 1: Service Extraction ---")
        mock_model_instance.generate_content.return_value.text = "shoe"
        
        result = llm_service.extract_keyword("I need a shoe")
        print(f"Result: {result}")
        
        if result == "shoe":
            print("PASS: Service extracted 'shoe'")
        else:
            print(f"FAIL: Expected 'shoe', got '{result}'")

def test_data_loader_integration():
    print("\nTesting Data Loader Integration...")
    
    from app.services.data_loader import data_loader
    from app.services.llm_service import llm_service
    
    # Mock the llm_service.extract_keyword method
    with patch.object(llm_service, 'extract_keyword', return_value="pharmacy") as mock_extract:
        # Mock raw search
        with patch.object(data_loader, '_search_products_raw') as mock_raw_search:
            mock_raw_search.return_value = [{"line_name": "Pharmacy Line"}]
            
            results = data_loader.search_products("Where is the pharmacy?")
            
            mock_extract.assert_called_with("Where is the pharmacy?")
            mock_raw_search.assert_called_with("pharmacy")
            print("PASS: Data Loader used LLM Service")

if __name__ == "__main__":
    test_llm_service()
    test_data_loader_integration()
