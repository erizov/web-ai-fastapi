# app/routes/vacancy.py

from fastapi import APIRouter, Body
from app.services.vacancy import generate_vacancy_description

router = APIRouter()

@router.post("/generate")
async def generate(vacancy_data: dict[str, str] = Body(...)):
    description = await generate_vacancy_description(vacancy_data)
    return {"vacancy_description": description}