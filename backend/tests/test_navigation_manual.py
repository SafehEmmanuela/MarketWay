import sys
import os
import json

# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.navigation_service import navigation_service
from app.api.api import NavigateResponse

def test_navigation():
    print("Testing Navigation Service...")

    # Test Case 1: Mothers Line (Left, 1)
    print("\n--- Test Case 1: Mothers Line (Left, 1) ---")
    result = navigation_service.get_directions("Mothers Line")
    print(json.dumps(result, indent=2))
    
    if "Walk to the FIRST line on your left." not in result["steps"]:
        print("FAIL: Expected 'Walk to the FIRST line' step not found")
    else:
        print("PASS: Step found")

    # Test Case 2: Family Line (Left, 2)
    print("\n--- Test Case 2: Family Line (Left, 2) ---")
    result = navigation_service.get_directions("Family Line")
    print(json.dumps(result, indent=2))
    
    expected_landmark = "Walk past Mothers Line."
    if expected_landmark not in result["steps"]:
        print(f"FAIL: Expected '{expected_landmark}' not found")
    else:
        print("PASS: Landmark step found")

    # Test Case 3: Magazine Line (Left, 3)
    print("\n--- Test Case 3: Magazine Line (Left, 3) ---")
    result = navigation_service.get_directions("Magazine Line")
    print(json.dumps(result, indent=2))
    
    expected_landmark_2 = "Walk past Mothers Line, Family Line."
    if expected_landmark_2 not in result["steps"]:
        print(f"FAIL: Expected '{expected_landmark_2}' not found")
    else:
        print("PASS: Multi-landmark step found")

    # Test Case 4: API Model Validation
    print("\n--- Test Case 4: API Model Validation ---")
    try:
        model = NavigateResponse(**result)
        print("Model validation successful")
    except Exception as e:
        print(f"FAIL: Model validation failed: {e}")

if __name__ == "__main__":
    test_navigation()
