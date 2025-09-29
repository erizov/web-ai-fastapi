from fastapi import FastAPI
from app.routes import vacancy

app = FastAPI(title="FastAPI HW1: Vacancy Parser with OpenAI Proxy and Tests")

app.include_router(vacancy.router)
