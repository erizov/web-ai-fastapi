from pydantic import BaseModel, EmailStr, field_validator

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    age: int

    @field_validator("username")
    def username_length(cls, v):
        if not (3 <= len(v) <= 20):
            raise ValueError("Username length must be between 3 and 20 characters")
        return v
