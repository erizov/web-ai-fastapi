# app/routes/examples.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "This is examples!"}