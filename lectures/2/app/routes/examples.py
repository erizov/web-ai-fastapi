# app/routes/examples.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()

# ==========================================================
# 1. Типизация: целое число
# Здесь мы объявляем маршрут GET, который принимает параметр `x` из URL.
# Типизация (x: int) говорит FastAPI автоматически преобразовать строку в число.
# Возвращаем словарь, где ключ "result" — это квадрат числа.
# ==========================================================
@router.get("/square/{x}")
def square(x: int) -> dict:
    return {"result": x * x}


# ==========================================================
# 2. Типизация: список чисел
# Этот маршрут принимает POST-запрос с JSON-массивом чисел.
# FastAPI автоматически преобразует JSON-массив в список Python.
# Функция считает сумму всех чисел и возвращает её.
# ==========================================================
@router.post("/sum")
def calc_sum(numbers: list[int]) -> dict:
    return {"sum": sum(numbers)}


# ==========================================================
# 3. Pydantic: простая модель
# Здесь мы используем Pydantic-модель для описания структуры входных данных.
# В JSON ожидаются поля `id` (int) и `name` (str).
# Если данные не соответствуют типам — FastAPI вернёт ошибку 422.
# ==========================================================
class User(BaseModel):
    id: int
    name: str

@router.post("/user")
def create_user(user: User) -> dict:
    return {"msg": f"User {user.name} created"}


# ==========================================================
# 4. Pydantic: вложенные модели
# Здесь показываем, что модели могут содержать другие модели.
# Поле `address` — это объект с `city` и `street`.
# Вложенность помогает описывать сложные структуры JSON.
# ==========================================================
class Address(BaseModel):
    city: str
    street: str

class Person(BaseModel):
    name: str
    address: Address

@router.post("/person")
def add_person(person: Person) -> dict:
    return {"msg": f"{person.name} lives in {person.address.city}"}


# ==========================================================
# 5. Валидация: email
# Pydantic имеет встроенные валидаторы, например EmailStr.
# Если в поле email придёт строка без символа '@', то сразу вернётся ошибка 422.
# ==========================================================
class Contact(BaseModel):
    email: EmailStr

@router.post("/contact")
def add_contact(contact: Contact):
    return {"msg": f"Email {contact.email} accepted"}


# ==========================================================
# 6. Валидация: ограничение строки
# С помощью `Field` можно ограничить минимальную и максимальную длину строки.
# Если строка слишком короткая или длинная, FastAPI вернёт ошибку 422.
# ==========================================================
class Note(BaseModel):
    text: str = Field(..., min_length=5, max_length=50)

@router.post("/note")
def create_note(note: Note):
    return {"note": note.text}


# ==========================================================
# 7. Валидация: диапазон числа
# `Field(ge=1, le=5)` означает, что число должно быть целым от 1 до 5.
# Если придёт 0 или 6 — FastAPI вернёт 422.
# ==========================================================
class Rating(BaseModel):
    value: int = Field(..., ge=1, le=5)

@router.post("/rate")
def rate_item(rating: Rating):
    return {"rating": rating.value}


# ==========================================================
# 8. Валидация: список строк
# `Field(min_items=1, max_items=5)` позволяет задать ограничения для списка:
# - min_items=1 (минимум один элемент)
# - max_items=5 (не больше пяти элементов)
# ==========================================================
class Tags(BaseModel):
    tags: list[str] = Field(..., min_items=1, max_items=5)

@router.post("/tags")
def add_tags(data: Tags):
    return {"tags": data.tags}


# ==========================================================
# 9. Ошибки: деление на ноль (400)
# Иногда нужно явно обработать ошибку, например, деление на ноль.
# В таком случае мы выбрасываем HTTPException с кодом 400 (Bad Request).
# ==========================================================
@router.get("/divide")
def divide(x: int, y: int):
    if y == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": x / y}


# ==========================================================
# 10. Ошибки: пользователь не найден (404)
# Если пользователь не существует, возвращаем 404 Not Found.
# HTTPException даёт нам контроль над статусом и текстом ошибки.
# ==========================================================
@router.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": 1, "name": "Alice"}


