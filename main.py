"""Точка входа: веб-сервер на FastAPI.

Здесь только «маршруты» — какой адрес что делает. Работа с документом
вынесена в пакет app/docx_builder, работа с базой — в app/routers/programs.py.

Запуск:  python main.py
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routers import programs
from app.schemas import RPDGenerateRequest

# Папка проекта. Пути считаем от неё, чтобы сервер работал при запуске из любого места.
BASE_DIR = Path(__file__).resolve().parent

# logging — стандартная замена print: у сообщений есть время, уровень
# (INFO, ERROR) и их можно направить в файл, не меняя код.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Код до yield выполняется один раз при старте сервера, после yield — при остановке."""
    init_db()
    yield


app = FastAPI(title="Конструктор РПД", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(programs.router)
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/")
def root(request: Request) -> Response:
    """Главная страница: форма создания программы."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/programs")
def programs_page(request: Request) -> Response:
    """Страница со списком сохранённых программ."""
    return templates.TemplateResponse(request, "programs.html")


@app.post("/generate-word")
def generate_word(data: RPDGenerateRequest) -> Response:
    """Принимает данные формы и сразу возвращает .docx, ничего не сохраняя.

    Параметр data объявлен с типом RPDGenerateRequest — этого достаточно, чтобы
    FastAPI сам разобрал JSON, проверил его и при ошибке ответил кодом 422.

    Функция объявлена через def, а не async def: сборка документа занимает
    процессор, и FastAPI выполнит её в отдельном потоке, не блокируя остальные запросы.
    """
    return programs.docx_response(data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
