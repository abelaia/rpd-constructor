"""Разделы, состоящие только из текста: I, II, VII и IX."""

from docx.document import Document

from app.schemas import SectionContents

from .helpers import add_blank, add_heading, add_text_block


def add_goals(doc: Document, contents: SectionContents) -> None:
    """Раздел I. Цели и задачи."""
    add_heading(doc, "I. ЦЕЛИ И ЗАДАЧИ ОСВОЕНИЯ ДИСЦИПЛИНЫ")
    add_blank(doc)
    add_text_block(doc, contents.I, placeholder="Текст раздела не введен.", bullets=True)


def add_place_in_program(doc: Document, contents: SectionContents) -> None:
    """Раздел II. Место дисциплины в образовательной программе."""
    add_heading(doc, "II. МЕСТО ДИСЦИПЛИНЫ В СТРУКТУРЕ ОБРАЗОВАТЕЛЬНОЙ ПРОГРАММЫ")
    add_blank(doc)
    add_text_block(doc, contents.II, placeholder="Текст раздела не введен.", bullets=True)


def add_guidelines(doc: Document, contents: SectionContents) -> None:
    """Раздел VII. Методические указания."""
    add_heading(doc, "VII. МЕТОДИЧЕСКИЕ УКАЗАНИЯ ДЛЯ ОБУЧАЮЩИХСЯ ПО ОСВОЕНИЮ ДИСЦИПЛИНЫ")
    add_blank(doc)
    add_text_block(doc, contents.VII, placeholder="Методические указания не введены.")


def add_final_provisions(doc: Document, contents: SectionContents) -> None:
    """Раздел IX. Заключительные положения."""
    add_heading(doc, "IX. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ")
    add_blank(doc)
    add_text_block(doc, contents.IX, placeholder="Дополнительная информация не указана.")
