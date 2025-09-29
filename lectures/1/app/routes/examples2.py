# app/routes/examples2.py

from fastapi import APIRouter, Path, Query, Body, Form, Header, Cookie, WebSocket
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse

router = APIRouter()

# 1️⃣ Простой GET
# Возвращает простой словарь, пример базового маршрута
# Используется для проверки доступности сервера
@router.get("/hello")
def hello():
    return {"message": "Hello, World!"}

# 2️⃣ GET с query-параметрами
# Query — параметры после ? в URL, можно задавать описание и дефолтное значение
# Пример: /greet?name=Alex&age=30
@router.get("/greet")
def greet(name: str = Query("Guest", description="Имя пользователя"), age: int = Query(18, description="Возраст пользователя")):
    return {"greeting": f"Привет, {name}! Тебе {age} лет."}

# 3️⃣ GET с path-параметром
# Path — часть URL, пример /user/42
# Используется для получения данных по ID
@router.get("/user/{user_id}")
def get_user(user_id: int = Path(..., description="ID пользователя")):
    return {"user_id": user_id, "name": f"User{user_id}"}

# 4️⃣ GET с path-параметром с регулярным выражением
# Позволяет ограничить формат параметра (только цифры)
# Пример: /order/123
@router.get("/order/{order_id}")
def get_order(order_id: str = Path(..., regex="^[0-9]+$", description="ID заказа, только цифры")):
    return {"order_id": order_id}

# 5️⃣ POST с словарём в body
# Body — данные POST запроса, передаются как JSON
# Возвращает присланные данные обратно
@router.post("/echo")
def echo(data: dict = Body(..., description="Любые данные в формате JSON")):
    return {"you_sent": data}

# 6️⃣ POST, возвращаем текст
# Пример возврата PlainTextResponse
# Можно использовать для отправки простого текста
@router.post("/text")
def post_text(data: dict = Body(...)):
    message = data.get("message", "No message")
    return PlainTextResponse(f"Твой текст: {message}")

# 7️⃣ GET с query и default
# Демонстрация суммирования чисел через query
# Пример: /sum?a=5&b=7
@router.get("/sum")
def sum_numbers(a: int = Query(..., description="Первое число"), b: int = Query(0, description="Второе число, по умолчанию 0")):
    return {"a": a, "b": b, "sum": a + b}

# 8️⃣ GET с Path + Query
# Получаем элемент по ID и дополнительный query параметр
# Пример: /items/99?q=test
@router.get("/items/{item_id}")
def read_item(item_id: int = Path(..., description="ID элемента"), q: str = Query(None, description="Дополнительный параметр")):
    return {"item_id": item_id, "query": q}

# 9️⃣ POST с JSONResponse
# Возвращает JSON с добавленным статусом
# Пример создания объекта
@router.post("/create")
def create_object(data: dict = Body(...)):
    data["status"] = "created"
    return JSONResponse(content=data)

# 1️⃣0️⃣ GET с булевым query
# Демонстрация включения/отключения функции
# Пример: /feature?enabled=false
@router.get("/feature")
def feature(enabled: bool = Query(True, description="Включение функции")):
    return {"feature_enabled": enabled}

# 1️⃣1️⃣ GET с optional query
# Параметр передаётся через query, не обязателен
# Пример: /optional?name=Alex
@router.get("/optional")
def optional_name(name: str = Query(None, description="Имя пользователя")):
    if name:
        return {"message": f"Привет, {name}!"}
    return {"message": "Привет, незнакомец!"}

# 1️⃣2️⃣ GET с массивом query
# Можно передавать несколько значений одного параметра
# Пример: /tags?tags=red&tags=blue
@router.get("/tags")
def get_tags(tags: list[str] = Query([], description="Список тегов")):
    return {"tags": tags}

# 1️⃣3️⃣ POST с массивом словарей
# Принимаем список объектов и возвращаем количество и сами объекты
@router.post("/bulk")
def bulk_create(items: list[dict] = Body(..., description="Список объектов")):
    return {"count": len(items), "items": items}

# 1️⃣4️⃣ GET с заголовком
# Чтение значения заголовка X-Token
@router.get("/header")
def read_header(x_token: str = Header(None, description="Значение заголовка X-Token")):
    return {"X-Token": x_token}

# 1️⃣5️⃣ GET с кукой
# Чтение куки с именем my_cookie
@router.get("/cookie")
def read_cookie(my_cookie: str = Cookie(None, description="Пример cookie")):
    return {"my_cookie": my_cookie}

# 1️⃣6️⃣ POST с формой
# Чтение данных из формы (Form)
# Требует установки python-multipart
@router.post("/login")
def login(username: str = Form(..., description="Имя пользователя"), password: str = Form(..., description="Пароль")):
    return {"username": username, "password_length": len(password)}

# 1️⃣7️⃣ GET с редиректом
# Перенаправление на другой маршрут
@router.get("/redirect")
def redirect_example():
    return RedirectResponse(url="/examples/hello")

# 1️⃣8️⃣ GET с динамическим форматом
# Возвращает текст или JSON в зависимости от path-параметра
# Пример: /dynamic/json или /dynamic/text
@router.get("/dynamic/{format}")
def dynamic_response(format: str = Path(..., description="Формат ответа: text/json")):
    if format == "text":
        return PlainTextResponse("Простой текст")
    elif format == "json":
        return {"message": "JSON сообщение"}
    else:
        return JSONResponse(content={"message": "Дефолтный JSON"})

# 1️⃣9️⃣ GET с optional query и default
# Пример поиска с лимитом
@router.get("/search")
def search(q: str = Query("fastapi", description="Строка поиска"), limit: int = Query(10, description="Лимит результатов")):
    return {"query": q, "limit": limit}

# 2️⃣0️⃣ POST с вложенным словарем
# Принимаем nested dict в body
@router.post("/nested")
def nested_dict(data: dict = Body(..., description="Вложенный словарь")):
    nested = data.get("nested", {})
    return {"received_nested": nested}

# 2️⃣1️⃣ GET с path int + validation
# Ограничиваем возраст 0-120
@router.get("/age/{age}")
def age_check(age: int = Path(..., ge=0, le=120, description="Возраст от 0 до 120")):
    return {"age": age, "status": "valid" if 0 <= age <= 120 else "invalid"}

# 2️⃣2️⃣ GET с проверкой авторизации
# Header Authorization: Bearer <token>
# Проверяем токен, возвращаем доступ/ошибку
@router.get("/protected")
def protected_route(authorization: str = Header(None, description="Authorization: Bearer <token>")):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    token = authorization.split(" ")[1]
    if token != "mysecrettoken":
        return JSONResponse(content={"error": "Invalid token"}, status_code=403)
    return {"message": "Access granted", "token": token}

# 2️⃣3️⃣
# WebSocket
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    try:
        while True:
            data = await websocket.receive_text()
            print(f'Принято: {data}')
    except:
        print("Client disconnected")