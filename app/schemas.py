from pydantic import BaseModel

# This handles the data COMING FROM the frontend
class ChatRequest(BaseModel):
    query: str

# This handles the data GOING TO the frontend
class ChatResponse(BaseModel):
    status: str
    data: str