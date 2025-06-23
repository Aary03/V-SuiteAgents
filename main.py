from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from orch import valura_team
import json

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates directory for HTML rendering
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# @app.get("/", response_class=HTMLResponse)
# async def get_chat(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/api/chat", response_model=ChatResponse)
# async def chat_endpoint(chat_request: ChatRequest):
#     run_response = valura_team.run(
#         chat_request.message,
#         session_id=chat_request.session_id
#     )
#     # run_response is a TeamRunResponse, get the string content
#     response_text = run_response.get_content_as_string() if run_response else "No response."
#     return ChatResponse(response=response_text, session_id=chat_request.session_id or "session")

@app.post("/api/chat/stream")
def chat_stream_endpoint(chat_request: ChatRequest):
    def event_stream():
        for chunk in valura_team.run(
            chat_request.message,
            session_id=chat_request.session_id,
            stream=True,
            stream_intermediate_steps=True
        ):
            # Handle different types of events in the stream
            content = None
            event_type = getattr(chunk, 'event', None)
            
            # Handle different types of responses
            if hasattr(chunk, 'get_content_as_string'):
                content = chunk.get_content_as_string()
            elif hasattr(chunk, 'content'):
                content = chunk.content
            elif isinstance(chunk, str):
                content = chunk
            
            # Send the event data
            if content is not None or event_type is not None:
                yield f"data: {json.dumps({'content': content, 'event': event_type})}\n\n"
                
    return StreamingResponse(event_stream(), media_type="text/event-stream") 