import json
import os
from typing import Dict, List, Optional
from pypdf import PdfReader
from app.core.config import settings
from .llm_service import llm_service
from .navigation_service import navigation_service

class DataLoader:
    def __init__(self):
        self.market_data: Dict = {}
        self.history_text: str = ""
        self.lines: List[Dict] = []
        self.lines_by_id: Dict[str, Dict] = {}  # Fast lookup by line ID
        self._load_data()

    def _load_data(self):
        """Load market data from JSON file with new flat structure"""
        # Load JSON
        if os.path.exists(settings.JSON_PATH):
            try:
                with open(settings.JSON_PATH, 'r') as f:
                    self.market_data = json.load(f)
                    print(f"Loaded market data: {len(self.market_data)} lines")

                    # Process flat structure where each key is a line ID
                    self.lines = []
                    self.lines_by_id = {}
                    
                    for line_id, line_data in self.market_data.items():
                        # Enrich line data with the line_id for easy reference
                        enriched_line = {
                            "line_id": line_id,
                            "line_name": line_data.get("line_name", ""),
                            "aisle": line_data.get("aisle", 0),
                            "items_sold": line_data.get("items_sold", []),
                            "order": line_data.get("order", 999)
                        }
                        
                        self.lines.append(enriched_line)
                        self.lines_by_id[line_id] = enriched_line

                    # Sort lines by aisle first, then by order within aisle
                    self.lines.sort(key=lambda x: (x["aisle"], x["order"]))
                    
                    print(f"Processed {len(self.lines)} lines across {len(set(l['aisle'] for l in self.lines))} aisles")

            except Exception as e:
                print(f"Error loading JSON: {e}")
                self.market_data = {}
                self.lines = []
                self.lines_by_id = {}
        else:
            print(f"Warning: JSON file not found at {settings.JSON_PATH}")

        # Load PDF
        if os.path.exists(settings.PDF_PATH):
            try:
                reader = PdfReader(settings.PDF_PATH)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                self.history_text = text
            except Exception as e:
                print(f"Error loading PDF: {e}")
                self.history_text = "Error loading history data."
        else:
            print(f"Warning: PDF file not found at {settings.PDF_PATH}")
            self.history_text = "History data not available (PDF missing)."

    def get_all_lines(self) -> List[Dict]:
        """Get all lines sorted by aisle and order"""
        return self.lines

    def get_line_by_id(self, line_id: str) -> Optional[Dict]:
        """Fast lookup by line ID (e.g., 'l1', 'l2', 'li', etc.)"""
        return self.lines_by_id.get(line_id)

    def get_line_by_name(self, name: str) -> Optional[Dict]:
        """Find line by name (case-insensitive)"""
        name_lower = name.lower()
        for line in self.lines:
            if line.get("line_name", "").lower() == name_lower:
                return line
        return None

    def get_lines_by_aisle(self, aisle_number: int) -> List[Dict]:
        """Get all lines in a specific aisle, sorted by order"""
        aisle_lines = [line for line in self.lines if line["aisle"] == aisle_number]
        return sorted(aisle_lines, key=lambda x: x["order"])

    def search_products(self, query: str) -> dict:
        """
        Search for products across all lines.
        Returns matching lines with directions based on aisle and order.
        """
        results = []
        
        # Extract keyword using LLM
        keyword = llm_service.extract_keyword(query=query).lower()
        print(f"Search keyword: '{keyword}'")
        
        for line in self.lines:
            line_name = line.get("line_name", "")
            items = line.get("items_sold", [])
            aisle = line.get("aisle", 0)
            order = line.get("order", 0)

            # Check if keyword matches line name
            if keyword in line_name.lower():
                results.append({
                    **line,
                    "match_type": "line_name",
                    "matched_term": line_name,
                    "direction": self._get_direction(aisle, order)
                })
                break

            # Check if keyword matches any item
            for item in items:
                if keyword in item.lower():
                    results.append({
                        **line,
                        "match_type": "item",
                        "matched_term": item,
                        "direction": self._get_direction(aisle, order)
                    })
                    break  # Only add line once even if multiple items match
            
            # Stop after first match for faster results
            if len(results) > 0:
                break
        
        direction = navigation_service.navigate(results[0]) if results else ""

        return {"direction": direction, "name": line_name[:-4].strip()} 

    def search_products_all_matches(self, query: str) -> List[Dict]:
        """
        Search for products and return ALL matching lines (not just first).
        Useful when user wants to see all options.
        """
        results = []
        
        keyword = llm_service.extract_keyword(query=query).lower()
        print(f"Search keyword (all matches): '{keyword}'")
        
        for line in self.lines:
            line_id = line.get("line_id", "")
            line_name = line.get("line_name", "")
            items = line.get("items_sold", [])
            aisle = line.get("aisle", 0)
            order = line.get("order", 0)

            # Check line name match
            if keyword in line_name.lower():
                results.append({
                    **line,
                    "match_type": "line_name",
                    "matched_term": line_name,
                    "direction": self._get_direction(aisle, order)
                })
                continue

            # Check item matches
            matched_items = [item for item in items if keyword in item.lower()]
            if matched_items:
                results.append({
                    **line,
                    "match_type": "item",
                    "matched_term": ", ".join(matched_items),
                    "direction": self._get_direction(aisle, order)
                })
        
        return results

    def _get_direction(self, aisle: int, order: int) -> str:
        """
        Generate human-readable directions based on aisle and order.
        """
        direction = f"Aisle {aisle}, Position {order}"
        
        # Add relative position hints
        if order <= 3:
            position = "near the beginning"
        elif order <= 7:
            position = "in the middle"
        else:
            position = "towards the end"
        
        return f"{direction} ({position} of aisle {aisle})"


    def get_history(self) -> str:
        """Get market history text from PDF"""
        return self.history_text


# Global instance
data_loader = DataLoader()