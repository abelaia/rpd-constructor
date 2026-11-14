"""Точка входа: веб-сервер на FastAPI.

Здесь только «маршруты» — какой адрес что делает. Вся работа с документом
вынесена в пакет app/docx_builder.

Запуск:  python main.py
"""

import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.docx_builder import build_rpd
from app.filenames import build_filename
from app.schemas import RPDGenerateRequest

# Папка проекта. Пути считаем от неё, чтобы сервер работал при запуске из любого места.
BASE_DIR = Path(__file__).resolve().parent
DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# logging — стандартная замена print: у сообщений есть время, уровень
# (INFO, ERROR) и их можно направить в файл, не меняя код.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("rpd")

app = FastAPI(title="Конструктор РПД")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/")
def root(request: Request) -> Response:
    """Главная страница."""
    return templates.TemplateResponse(request, "index.html")


@app.post("/generate-word")
def generate_word(data: RPDGenerateRequest) -> Response:
    """Принимает данные формы и возвращает готовый .docx.

    Параметр data объявлен с типом RPDGenerateRequest — этого достаточно, чтобы
    FastAPI сам разобрал JSON, проверил его и при ошибке ответил кодом 422.

    Функция объявлена через def, а не async def: сборка документа занимает
    процессор, и FastAPI выполнит её в отдельном потоке, не блокируя остальные запросы.
    """
    try:
        content = build_rpd(data)
    except Exception as error:
        # Подробности пишем в журнал сервера, пользователю — короткое сообщение.
        logger.exception("Не удалось сформировать документ «%s»", data.discipline_name)
        raise HTTPException(status_code=500, detail="Не удалось сформировать документ") from error

    filename = build_filename(data.custom_filename, data.discipline_name)
    logger.info("Сформирован документ %s", filename)
    return Response(
        content=content,
        media_type=DOCX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
