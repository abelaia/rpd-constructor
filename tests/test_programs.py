"""Тесты API сохранённых программ: создание, список, чтение, изменение, удаление."""

from docx_dump import dump_docx


def create(client, payload) -> dict:
    response = client.post("/api/programs", json=payload)
    assert response.status_code == 201
    return response.json()


def test_list_is_empty_at_start(client):
    response = client.get("/api/programs")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_read_program(client, full_payload):
    created = create(client, full_payload)

    assert created["discipline_name"] == "Web Development (Веб-разработка)"
    assert created["teacher_name"] == "И. И. Иванов"
    # Время отдаётся с пометкой UTC, чтобы браузер показал его в местном поясе.
    assert created["created_at"].endswith("Z")

    saved = client.get(f"/api/programs/{created['id']}").json()
    assert saved["data"]["department"] == "Тестовая кафедра"
    assert saved["data"]["section_contents"]["IV_table"][1]["points"] == "10"
    assert len(saved["data"]["toc_items"]) == 3


def test_list_shows_recent_first(client, full_payload):
    first = create(client, full_payload)
    second = create(client, {"discipline_name": "Физика"})

    programs = client.get("/api/programs").json()

    assert [p["id"] for p in programs] == [second["id"], first["id"]]
    # В списке только краткие сведения, без содержимого программы.
    assert "data" not in programs[0]


def test_update_program(client, full_payload):
    created = create(client, full_payload)
    full_payload["discipline_name"] = "Web Development 2.0"
    full_payload["section_contents"]["IX"] = "Новый текст"

    response = client.put(f"/api/programs/{created['id']}", json=full_payload)

    assert response.status_code == 200
    assert response.json()["discipline_name"] == "Web Development 2.0"
    saved = client.get(f"/api/programs/{created['id']}").json()
    assert saved["data"]["section_contents"]["IX"] == "Новый текст"
    assert len(client.get("/api/programs").json()) == 1


def test_delete_program(client, full_payload):
    created = create(client, full_payload)

    assert client.delete(f"/api/programs/{created['id']}").status_code == 204
    assert client.get(f"/api/programs/{created['id']}").status_code == 404
    assert client.get("/api/programs").json() == []


def test_unknown_program_returns_404(client, full_payload):
    assert client.get("/api/programs/999").status_code == 404
    assert client.put("/api/programs/999", json=full_payload).status_code == 404
    assert client.delete("/api/programs/999").status_code == 404
    assert client.get("/api/programs/999/docx").status_code == 404


def test_invalid_program_is_not_saved(client):
    assert client.post("/api/programs", json={"discipline_name": ""}).status_code == 422
    assert client.get("/api/programs").json() == []


def test_saved_program_gives_same_document(client, full_payload):
    """Документ из базы должен совпадать с документом, собранным напрямую из формы."""
    created = create(client, full_payload)

    from_database = client.get(f"/api/programs/{created['id']}/docx")
    direct = client.post("/generate-word", json=full_payload)

    assert from_database.status_code == 200
    assert from_database.headers["content-disposition"] == direct.headers["content-disposition"]
    assert dump_docx(from_database.content) == dump_docx(direct.content)


def test_programs_page_opens(client):
    response = client.get("/programs")
    assert response.status_code == 200
    assert "Сохранённые программы" in response.text
