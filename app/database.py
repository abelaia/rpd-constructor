"""Подключение к базе данных.

Используем SQLite — база хранится в одном файле, отдельный сервер не нужен.
С базой работаем через SQLAlchemy: это ORM, то есть строки таблиц в коде
выглядят как обычные объекты Python, а SQL-запросы библиотека пишет сама.

Три главных понятия SQLAlchemy:
  engine  — подключение к базе (одно на всё приложение);
  session — «рабочая сессия»: в ней читаем и меняем объекты, а commit()
            сохраняет изменения в базу одной транзакцией;
  Base    — общий предок всех моделей (описаний таблиц).
"""

import json
import os
from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'data' / 'rpd.db'}"

# Адрес базы можно переопределить переменной окружения — пригодится при переходе
# на PostgreSQL: код менять не придётся.
DATABASE_URL = os.environ.get("RPD_DATABASE_URL", DEFAULT_DATABASE_URL)


def _to_json(value: object) -> str:
    """Сохраняет кириллицу как есть, а не в виде \\u0440\\u0443..., чтобы базу можно было читать."""
    return json.dumps(value, ensure_ascii=False)


def make_engine(url: str = DATABASE_URL, **kwargs):
    """Создаёт подключение. Вынесено в функцию, чтобы тесты могли подключить свою базу."""
    return create_engine(
        url,
        json_serializer=_to_json,
        # SQLite по умолчанию запрещает использовать соединение из другого потока,
        # а FastAPI обрабатывает запросы в нескольких потоках.
        connect_args={"check_same_thread": False},
        **kwargs,
    )


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Общий предок моделей. SQLAlchemy собирает через него список всех таблиц."""


def init_db() -> None:
    """Создаёт файл базы и таблицы, если их ещё нет. Вызывается при старте сервера."""
    if DATABASE_URL == DEFAULT_DATABASE_URL:
        (BASE_DIR / "data").mkdir(exist_ok=True)
    # Импорт нужен, чтобы модели «зарегистрировались» в Base до создания таблиц.
    from app import models  # noqa: F401

    Base.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Выдаёт сессию на время одного запроса и закрывает её после ответа.

    FastAPI вызывает эту функцию сам для каждого маршрута, где указано
    Depends(get_session). Такой приём называется «внедрение зависимостей».
    """
    with SessionLocal() as session:
        yield session
