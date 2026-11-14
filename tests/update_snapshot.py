"""Пересоздаёт эталон документа для теста test_full_document_matches_snapshot.

Запускать из корня проекта, когда документ изменён намеренно:
    python tests/update_snapshot.py
После запуска посмотрите разницу через git diff и убедитесь, что она ожидаемая.
"""

import json
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).parent
sys.path.insert(0, str(TESTS_DIR.parent))

from docx_dump import dump_docx  # noqa: E402

from app.docx_builder import build_rpd  # noqa: E402
from app.schemas import RPDGenerateRequest  # noqa: E402

payload = json.loads((TESTS_DIR / "fixtures" / "full_rpd.json").read_text(encoding="utf-8"))
content = build_rpd(RPDGenerateRequest(**payload), year=2026)

snapshot = TESTS_DIR / "snapshots" / "full_rpd.txt"
snapshot.parent.mkdir(exist_ok=True)
snapshot.write_text(dump_docx(content), encoding="utf-8", newline="\n")
print(f"Эталон обновлён: {snapshot}")
