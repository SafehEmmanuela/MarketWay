from .router_service import router_service
from .data_loader import data_loader
from .info_service import info_service
from typing import Dict


def get_intent_and_execute(message: str) -> Dict[str, str]:
    return execute(router_service.route(message))


def execute(router_info: dict) -> dict:
    action = router_info.get("action")
    if action == "search":
        # Perform search action
        query = router_info.get("query", "")
        return data_loader.search_products(query)
    elif action == "info":
        topic = router_info.get("original_message", "")
        answer = info_service.search(topic)
        return {"info": answer}

# get_intent("Where can I get an umbrella?")