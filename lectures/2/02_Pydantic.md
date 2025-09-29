# Pydantic: создание схем (моделей) данных

## Введение

Pydantic — библиотека для работы с данными в Python.

### Главная идея:
👉 описали схему через Python-типы → получили автоматическую валидацию и преобразование данных.

Используется в:
- FastAPI (для входных/выходных моделей),
- скриптах (проверка входных JSON),
- конфигурациях (например, настройки проекта через .env).

### Простейший пример:

```
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

u = User(id="1", name="Alice")
print(u.id)        # 1 (автоматически привелось к int)
print(u.dict())    # {'id': 1, 'name': 'Alice'}
```

##  Создание моделей

### Базовая схема

```
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True
```

Особенности:
- поля описываются через аннотации типов;  
- значения по умолчанию → необязательные поля;  
- при создании объекта все данные проверяются.

### Обязательные и необязательные поля

```
from typing import Optional

class User(BaseModel):
    id: int
    email: Optional[str] = None
```

Optional → может быть None.

Если не указать = None, то параметр будет обязательным.

### Вложенные модели

```
class Address(BaseModel):
    city: str
    street: str

class Person(BaseModel):
    name: str
    address: Address

p = Person(name="Bob", address={"city": "Moscow", "street": "Tverskaya"})
print(p.address.city)  # "Moscow"
```

##  Валидация данных

### Автоматическая

```
class Order(BaseModel):
    quantity: int
    price: float

o = Order(quantity="5", price="12.5")  
print(o.price)  # 12.5 (строка преобразована в float)
```

## Ограниченные типы (Pydantic v2)

```
from pydantic import BaseModel, conint, constr

class Product(BaseModel):
    name: constr(min_length=3, max_length=50)
    quantity: conint(ge=1, le=100)
```

# Примеры:
```
product = Product(name="Laptop", quantity=5)
print(product.model_dump())   # словарь
print(product.model_dump_json())  # JSON
```

constr(min_length=3, max_length=50) → строка с ограничениями по длине  
conint(ge=1, le=100) → целое число в диапазоне от 1 до 100

## Валидаторы (кастомная логика)

```
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    # Валидатор для поля age
    @field_validator("age")
    def check_age(cls, v):
        if v < 0:
            raise ValueError("Возраст должен быть больше 0")
        return v
```

# Пример
```
user = User(name="Alice", age=25)
```

В Pydantic v2 используется @field_validator вместо @validator.

## Алиасы и переименование полей

```
from pydantic import BaseModel

class ConfigExample(BaseModel):
    user_id: int
    model_config = {
        "populate_by_name": True,
        "fields": {"user_id": {"alias": "userId"}}
    }

data = {"userId": 123}
obj = ConfigExample(**data)
print(obj.user_id)  # 123
```

alias позволяет использовать другие имена в JSON, но в коде работать с привычным именем.

## Чтение из .env

```
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    model_config = {
        "env_file": ".env"
    }

settings = Settings()
print(settings.database_url)
```

Позволяет хранить конфигурацию вне кода, безопасно для секретов.

##  Использование в FastAPI

### Входные данные (POST)

```
from fastapi import FastAPI
from pydantic import BaseModel, conint, constr

app = FastAPI()

class Item(BaseModel):
    name: constr(min_length=3, max_length=50)
    price: conint(ge=1)

@app.post("/items/")
def create_item(item: Item):
    return {"received": item.model_dump()}
```

FastAPI автоматически проверяет JSON.  
Если данные не проходят валидацию → возвращается 422 с ошибкой.

### Выходные данные (GET)

```
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int):
    # Можно вернуть лишние поля, они будут отброшены
    return {"id": user_id, "name": "Alice", "extra": "ignored"}
```

Swagger/Redoc автоматически покажет только поля модели.

## Заключение

Pydantic v2 + FastAPI позволяет:
1. Валидировать входные данные автоматически
2. Применять кастомную логику через field_validator
3. Ограничивать длину, диапазон чисел и форматы данных
4. Работать с JSON и словарями (model_dump, model_dump_json)
5. Использовать алиасы и конфигурацию через .env
6. FastAPI построен на Pydantic, но Pydantic можно использовать и отдельно от веб-приложений.
