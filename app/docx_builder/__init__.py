"""Сборка рабочей программы дисциплины в формате .docx.

Снаружи нужна одна функция — build_rpd. Она как оглавление: по ней видно,
из каких частей состоит документ и в каком порядке они идут. Каждая часть
лежит в своём файле этой папки.
"""

import io
from datetime import datetime

from docx import Document

from app.config import UNIVERSITY, University
from app.schemas import RPDGenerateRequest

from .assessment import add_assessment
from .competencies import add_competencies
from .helpers import add_section, setup_styles
from .resources import add_facilities, add_literature
from .structure import add_structure
from .text_sections import add_final_provisions, add_goals, add_guidelines, add_place_in_program
from .title_page import add_table_of_contents, add_title_page

__all__ = ["build_rpd"]


def build_rpd(
    data: RPDGenerateRequest,
    *,
    university: University = UNIVERSITY,
    year: int | None = None,
) -> bytes:
    """Собирает документ и возвращает его содержимое в виде байтов.

    year — год в строке «Программа одобрена на заседании кафедры»;
    по умолчанию берётся текущий.
    """
    contents = data.section_contents
    doc = Document()
    setup_styles(doc)

    add_title_page(doc, data, university, year or datetime.now().year)
    add_table_of_contents(doc, data)
    doc.add_page_break()

    add_goals(doc, contents)
    doc.add_page_break()
    add_place_in_program(doc, contents)

    # Разделы III и IV содержат широкие таблицы, поэтому идут на альбомных страницах.
    add_section(doc, landscape=True)
    add_competencies(doc, contents)
    doc.add_page_break()
    add_structure(doc, data)

    add_section(doc, landscape=False)
    add_literature(doc, contents)
    doc.add_page_break()
    add_facilities(doc, contents)
    doc.add_page_break()
    add_guidelines(doc, contents)
    doc.add_page_break()
    add_assessment(doc, contents)
    doc.add_page_break()
    add_final_provisions(doc, contents)

    # Документ сохраняем не на диск, а в память — сразу отдадим его в ответе.
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
