"""Общие заготовки для тестов.

Функции с @pytest.fixture — это «фикстуры»: pytest сам вызывает их и передаёт
результат в тест, если у теста есть параметр с таким же именем.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def client() -> TestClient:
    """Клиент, который шлёт запросы приложению напрямую, без запуска сервера."""
    return TestClient(app)


@pytest.fixture
def full_payload() -> dict:
    """Полностью заполненная рабочая программа."""
    return json.loads((FIXTURES / "full_rpd.json").read_text(encoding="utf-8"))
