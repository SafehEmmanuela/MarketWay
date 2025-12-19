from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Union
from app.services.chat_handler import get_intent_and_execute

class ItemSearchResponse(BaseModel):
    query: str
    direction: str
    name: str

class InfoSearchResponse(BaseModel):
    info: str

class ChatInterface:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get("/chat", response_model=Union[ItemSearchResponse, InfoSearchResponse])
        async def chat(q: str = Query(..., description="The user query")):
            result = get_intent_and_execute(q)
            if 'direction' in result:
                return ItemSearchResponse(
                    query=q,
                    direction=result.get("direction"),
                    name=result.get("name")
                )
            return InfoSearchResponse(info=result.get("info"))

# Instantiate the class and store in a variable named api
api = ChatInterface()
