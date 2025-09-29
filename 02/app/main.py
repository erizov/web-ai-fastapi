from fastapi import FastAPI, HTTPException
from app.models import UserRegister

app = FastAPI()

@app.post("/auth/register")
async def register_user(user: UserRegister):
    if user.username.lower() == "admin":
        raise HTTPException(status_code=400, detail="Username 'admin' is not allowed")
    if user.age < 18:
        raise HTTPException(status_code=400, detail="You must be at least 18 years old")
    return {
        "username": user.username,
        "email": user.email,
        "message": "User successfully registered"
    }
