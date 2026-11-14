"""Общие заготовки для тестов.

Функции с @pytest.fixture — это «фикстуры»: pytest сам вызывает их и передаёт
результат в тест, если у теста есть параметр с таким же именем.
"""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401 — регистрирует таблицы в Base
from app.database import Base, get_session, make_engine
from main import app

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Клиент, который шлёт запросы приложению напрямую, без запуска сервера.

    Для каждого теста создаётся своя пустая база в оперативной памяти,
    поэтому тесты не трогают настоящую базу и не влияют друг на друга.
    """
    # StaticPool — одно общее соединение: иначе у базы в памяти каждое
    # новое соединение видело бы свою отдельную пустую базу.
    engine = make_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    test_sessions = sessionmaker(bind=engine, expire_on_commit=False)

    def get_test_session() -> Iterator[Session]:
        with test_sessions() as session:
            yield session

    # Подменяем зависимость: маршруты получат сессию тестовой базы.
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def full_payload() -> dict:
    """Полностью заполненная рабочая программа."""
    return json.loads((FIXTURES / "full_rpd.json").read_text(encoding="utf-8"))
