"""Раздел VIII. Фонд оценочных средств."""

from docx.document import Document

from app.schemas import LabWork, SectionContents

from .helpers import (
    add_blank,
    add_heading,
    add_labeled_text,
    add_table,
    add_text,
    split_lines,
)

HEADERS_PASSPORT = (
    "№ п/п",
    "Код индикатора достижения компетенции",
    "Наименование оценочного средства",
)


def add_assessment(doc: Document, contents: SectionContents) -> None:
    add_heading(doc, "VIII. ФОНД ОЦЕНОЧНЫХ СРЕДСТВ")
    add_blank(doc)

    add_heading(doc, "8.1. Паспорт фонда оценочных средств", level=2)
    add_blank(doc)
    if contents.VIII_table:
        rows = [(r.num, r.code, r.name) for r in contents.VIII_table]
        add_table(doc, HEADERS_PASSPORT, rows)

    add_blank(doc)
    add_heading(doc, "8.2. Лабораторные работы", level=2)
    add_blank(doc)
    for lab in contents.VIII_labs:
        _add_lab(doc, lab)


def _add_lab(doc: Document, lab: LabWork) -> None:
    """Описание одной лабораторной работы; пустые поля пропускаются."""
    add_heading(doc, f"Лабораторная работа №{lab.number}", level=3)

    if lab.goal:
        add_labeled_text(doc, "Цель работы: ", lab.goal)
    if lab.tasks:
        add_labeled_text(doc, "Задачи: ", lab.tasks)
    if lab.theory:
        add_labeled_text(doc, "Теоретические сведения: ", lab.theory)
    if lab.steps:
        add_labeled_text(doc, "Порядок выполнения: ")
        for line in split_lines(lab.steps):
            add_text(doc, line, style="List Number")
    if lab.questions:
        add_labeled_text(doc, "Контрольные вопросы: ")
        for line in split_lines(lab.questions):
            add_text(doc, line, style="List Bullet")
    add_blank(doc)
