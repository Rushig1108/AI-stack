from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import requests
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Backend URL
BACKEND_URL = "http://backend-service:8000/process"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/query")
async def process_query(request: Request, query: str = Form(...)):
    response = requests.post(BACKEND_URL, json={"query": query})
    result = response.json().get("response", "Error processing request")
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "query": query})
