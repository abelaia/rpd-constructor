"""Превращает .docx в простой текст, чтобы документы можно было сравнивать в тестах.

Word-файл — это zip-архив с XML, сравнивать его байт в байт бессмысленно.
Поэтому мы проходим по документу сверху вниз и выписываем только то, что важно:
текст абзацев, их стиль и содержимое таблиц.
"""

import io

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def dump_docx(content: bytes) -> str:
    """Возвращает текстовое описание документа: по строке на абзац и на строку таблицы."""
    doc = Document(io.BytesIO(content))
    lines: list[str] = []

    for block in doc.iter_inner_content():
        if isinstance(block, Paragraph):
            if block.text.strip():
                lines.append(f"[{block.style.name}] {block.text}")
        elif isinstance(block, Table):
            lines.append("[Table]")
            for row in block.rows:
                # У объединённых ячеек python-docx возвращает одну и ту же ячейку
                # несколько раз подряд — оставляем по одной.
                cells: list[str] = []
                previous = None
                for cell in row.cells:
                    if previous is None or cell._tc is not previous:
                        cells.append(cell.text.replace("\n", " / "))
                    previous = cell._tc
                lines.append("  | " + " | ".join(cells))

    orientations = [str(section.orientation) for section in doc.sections]
    lines.append(f"[Sections] {', '.join(orientations)}")
    return "\n".join(lines) + "\n"
