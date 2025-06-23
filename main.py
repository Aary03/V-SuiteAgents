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

@app.get("/", response_class=JSONResponse)
async def health_check():
    return {"status": "ok"}

# @app.post("/api/chat", response_model=ChatResponse)
# async def chat_endpoint(chat_request: ChatRequest):
#     run_response = valura_team.run(
#         chat_request.message,
#         session_id=chat_request.session_id
#     )
#     # run_response is a TeamRunResponse, get the string content
#     response_text = run_response.get_content_as_string() if run_response else "No response."
#     return ChatResponse(response=response_text, session_id=chat_request.session_id or "session")

@app.post("/flask/api/chat/stream")
def chat_stream_endpoint(chat_request: ChatRequest):
    def event_stream():
        try:
            for chunk in valura_team.run(
                chat_request.message,
                session_id=chat_request.session_id,
                stream=True,
                stream_intermediate_steps=True
            ):
                # Skip ReasoningStep objects and other non-serializable types
                if hasattr(chunk, '__class__') and chunk.__class__.__name__ == 'ReasoningStep':
                    continue
                
                # Extract content and event type safely
                content = None
                event_type = getattr(chunk, 'event', None)
                
                # Handle different types of responses in order of preference
                if hasattr(chunk, 'get_content_as_string'):
                    content = chunk.get_content_as_string()
                elif hasattr(chunk, 'content'):
                    if isinstance(chunk.content, (str, int, float, bool, dict, list)):
                        content = chunk.content
                    else:
                        # If content is a complex object, try to get a string representation
                        try:
                            content = str(chunk.content)
                        except:
                            continue
                elif isinstance(chunk, (str, int, float, bool)):
                    content = chunk
                elif isinstance(chunk, (dict, list)):
                    content = chunk
                else:
                    # Skip any other non-serializable types
                    continue
                
                # Only yield if we have valid content or event type
                if content is not None or event_type is not None:
                    try:
                        event_data = {'content': content, 'event': event_type}
                        yield f"data: {json.dumps(event_data)}\n\n"
                    except Exception as e:
                        # If JSON serialization fails, try sending just the error
                        error_msg = {'content': f"Error processing response: {str(e)}", 'event': 'error'}
                        yield f"data: {json.dumps(error_msg)}\n\n"
                        
        except Exception as e:
            # Handle any errors in the main streaming loop
            error_msg = {'content': f"Streaming error: {str(e)}", 'event': 'error'}
            yield f"data: {json.dumps(error_msg)}\n\n"
                
    return StreamingResponse(event_stream(), media_type="text/event-stream")