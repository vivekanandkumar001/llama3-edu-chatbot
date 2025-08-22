from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

from .rag import get_rag_response
from .leads import save_lead

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def read_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    name = data.get("name", "")
    response = get_rag_response(user_message, name)
    return {"reply": response}


@app.post("/lead")
async def lead(name: str = Form(...), email: str = Form(""), phone: str = Form("")):
    save_lead(name, email, phone)
    return JSONResponse(content={"status": "saved"})
