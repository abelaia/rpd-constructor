"""Тесты генерации документа через HTTP — так же, как это делает браузер."""

from pathlib import Path

from docx_dump import dump_docx

from app.docx_builder import build_rpd
from app.schemas import RPDGenerateRequest

SNAPSHOT = Path(__file__).parent / "snapshots" / "full_rpd.txt"


def test_main_page_opens(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Конструктор РПД" in response.text


def test_full_document_matches_snapshot(full_payload):
    """Главный страховочный тест: документ не должен меняться незаметно.

    Эталон лежит в tests/snapshots/full_rpd.txt. Если документ изменён намеренно,
    эталон обновляется командой:  python tests/update_snapshot.py
    """
    content = build_rpd(RPDGenerateRequest(**full_payload), year=2026)
    assert dump_docx(content) == SNAPSHOT.read_text(encoding="utf-8")


def test_generate_returns_docx(client, full_payload):
    response = client.post("/generate-word", json=full_payload)

    assert response.status_code == 200
    assert response.headers["content-type"].endswith("wordprocessingml.document")
    assert response.headers["content-disposition"].startswith(
        'attachment; filename="RPD_Web Development_'
    )
    # .docx — это zip-архив, а zip всегда начинается с букв PK.
    assert response.content.startswith(b"PK")


def test_custom_filename_is_transliterated(client, full_payload):
    full_payload["custom_filename"] = "Моя программа"
    response = client.post("/generate-word", json=full_payload)
    assert response.headers["content-disposition"] == 'attachment; filename="Moia programma.docx"'


def test_minimal_request_works(client):
    """Достаточно одного названия: раньше такой запрос ронял сервер с ошибкой 500."""
    response = client.post("/generate-word", json={"discipline_name": "Физика"})

    assert response.status_code == 200
    text = dump_docx(response.content)
    assert "Текст раздела не введен." in text
    # В пустой документ не должны попадать чужие демонстрационные данные.
    assert "Spring" not in text
    assert "ОПК-1" not in text


def test_missing_discipline_name_is_rejected(client):
    response = client.post("/generate-word", json={})
    assert response.status_code == 422


def test_hyphens_inside_words_are_kept(client, full_payload):
    """Дефис в начале строки — маркер списка, дефис внутри слова — часть слова."""
    response = client.post("/generate-word", json=full_payload)
    text = dump_docx(response.content)

    assert "[List Bullet] изучить клиент-серверную архитектуру" in text
    assert "•" not in text


def test_totals_are_calculated(client, full_payload):
    response = client.post("/generate-word", json=full_payload)
    text = dump_docx(response.content)

    # Таблица 4.1: лекции 2+4, практические 1, лабораторные 2+4,
    # консультации 1, самостоятельная 4+6, баллы 10+15.
    assert "| Итого | 6 | 1 | 6 | 1 | 10 |  |  |  | 25" in text
    # Таблица 4.2: часы 10+12.
    assert "| Общая трудоёмкость самостоятельной работы по дисциплине | 22 | " in text
