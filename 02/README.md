# FastAPI HW2: Auth Project with Tests

## 📌 Requirements
- Python 3.9+
- FastAPI
- Uvicorn
- Requests
- Pytest

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Run the server
```bash
uvicorn app.main:app --reload
```

API docs:  
👉 http://127.0.0.1:8000/docs  
👉 http://127.0.0.1:8000/redoc

## 📝 API Endpoint

### Register User
**POST** `/auth/register`

#### Request Body
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "age": 25
}
```

#### Success (200)
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "message": "User successfully registered"
}
```

#### Errors
- Username 'admin' → 400 {"detail": "Username 'admin' is not allowed"}
- Age < 18 → 400 {"detail": "You must be at least 18 years old"}


## 🧪 Test with demo.py
Run server first:
```bash
uvicorn app.main:app --reload
```
Then run:
```bash
python demo.py
```

