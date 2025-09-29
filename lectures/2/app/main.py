# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
from .routes import examples, vacancy, auth
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()
    
# Создаём FastAPI приложение
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Подключаем роуты
app.include_router(examples.router, prefix="/examples", tags=["examples"])
app.include_router(vacancy.router, prefix="/vacancy", tags=["vacancy"])

# Запуск
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",      # 'app' путь, 'main' — имя файла без .py, второй 'app' — объект FastAPI
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True       # включаем авто-перезагрузку при изменении кода
    )