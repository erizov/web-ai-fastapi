# Введение в FastAPI

## Первое приложение на FastAPI

Давайте создадим простое приложение на FastAPI с маршрутом, который выводит "Hello, World!".

1. **Установка FastAPI и Uvicorn**:

Для начала нужно установить **FastAPI** и сервер **Uvicorn**. Для а файле requirements.txt пропишите библиотеки:

```
fastapi
uvicorn
```

Сделайте в терминале активным рабочий каталог `01`. Установите зависимости:
```
cd 01
pip install -r requirements.txt
```

2. **Создание приложения**:

Теперь создадим каталог `app`, в нем файл `main.py`:

```python
# app/main.py

from fastapi import FastAPI
import uvicorn

# Создаём FastAPI приложение
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
 
# Запуск
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",      # 'app' путь, 'main' — имя файла без .py, второй 'app' — объект FastAPI
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True       # включаем авто-перезагрузку при изменении кода
    )
```

3. **Запуск приложения**
```
python -m app.main
```

4. **Проверка работы**

Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/`  
Вы увидите следующий JSON-ответ:

```json
{"message": "Hello, World!"}
```

5. **Документация API**:

После того как приложение запущено, FastAPI автоматически генерирует документацию для вашего API. Вы можете найти её по адресу:

- http://127.0.0.1:8000/docs — для интерактивной документации.
- http://127.0.0.1:8000/redoc — для более статичной, но красивой документации.

В этих интерфейсах вы сможете увидеть все доступные маршруты вашего API, а также попробовать их прямо в браузере.

## Маршруты

Теперь в соответствии со структурой проекта в файл main.py добавим маршруты.

```python
# app/main.py

from fastapi import FastAPI
import uvicorn
from .routes import examples

# Создаём FastAPI приложение
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Подключаем роуты
app.include_router(examples.router, prefix="/examples", tags=["examples"])
 
# Запуск
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",      # 'main' — имя файла без .py, 'app' — объект FastAPI
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True       # включаем авто-перезагрузку при изменении кода
    )
```

И добавим обработку маршрутов, создав каталог `app/router`, а внутри него файл `examples.py`:

```python
# app/routes/examples.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "This is examples!"}
```

Протестируйте созданный маршрут в браузере:
```
http://127.0.0.1:8000/examples
```

## Примеры наиболее частых маршрутов

1. Возьмите из материалов курса файл examples2.py, добавьте его app/routes.
2. В файле main.py подключите файл examples2.py:
```
# app/main.py

from fastapi import FastAPI
import uvicorn
from .routes import examples, examples2

# Создаём FastAPI приложение
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Подключаем роуты
app.include_router(examples.router, prefix="/examples", tags=["examples"])
app.include_router(examples2.router, prefix="/examples", tags=["examples"])
 
# Запуск
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",      # 'main' — имя файла без .py, 'app' — объект FastAPI
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True       # включаем авто-перезагрузку при изменении кода
    )
```
3. Добавьте в requirements.txt модули:
```
...
requests
python-multipart
websockets
```

4. Остановите проект (если запущен) с помощью CTRL+C.
Если CTRL+C не реагирует - закройте терминал, откройте новый и перейдите в каталог `01`:
```
cd 01
```

5. Установите зависимости:
```
pip install -r requirements.txt
```

6. Запустите проект:
```
python -m app.main
```

7. Возьмите в материалах курса ноутбук examples.ipynb, скопируйте в каталог проекта `01` и запустите каждую ячейку ноутбука для тестирования.


