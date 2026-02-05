from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.controllers import SportsAIController

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # This takes the 'query' from the frontend, 
    # passes it to the controller, 
    # and returns the JSON result.
    return SportsAIController.process_query(request.query)