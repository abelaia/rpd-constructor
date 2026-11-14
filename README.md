# RPDConstructor — Конструктор рабочих программ дисциплин

Веб-приложение для создания рабочей программы дисциплины (РПД) по ГОСТ. Генерирует Word-документ с титульным листом, содержанием, таблицами и всеми разделами.

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

После запуска откройте http://localhost:8000

## Разработка

```bash
pip install -r requirements-dev.txt
pytest          # тесты
ruff check .    # проверка кода
ruff format .   # автоформатирование
```

## Структура

| Путь | Назначение |
|---|---|
| `main.py` | веб-сервер FastAPI: адреса страниц и запросов |
| `app/schemas.py` | описание данных, которые приходят с формы (Pydantic) |
| `app/config.py` | реквизиты вуза |
| `app/filenames.py` | имя скачиваемого файла |
| `app/docx_builder/` | сборка документа: по файлу на группу разделов РПД |
| `templates/`, `static/` | страница, стили и скрипты клиента |
| `tests/` | тесты; `tests/snapshots/` — эталон документа |
