"""Титульный лист и оглавление."""

from docx.document import Document
from docx.shared import Pt

from app.config import University
from app.schemas import RPDGenerateRequest

from .helpers import CENTER, LIST_INDENT, RIGHT, add_blank, add_text, style_run

# Позиция, по которой выравниваются номера страниц в оглавлении.
PAGE_NUMBER_TAB = Pt(450)


def add_title_page(
    doc: Document, data: RPDGenerateRequest, university: University, year: int
) -> None:
    """Титульный лист: вуз, название дисциплины, составитель, реквизиты утверждения."""
    add_text(doc, university.ministry, size=10, align=CENTER)
    add_text(doc, f"{university.full_name}\n({university.short_name})", align=CENTER)
    add_blank(doc, 5)

    add_text(doc, "РАБОЧАЯ ПРОГРАММА ДИСЦИПЛИНЫ (МОДУЛЯ)", size=14, bold=True, align=CENTER)
    add_text(doc, data.discipline_name, size=14, align=CENTER)
    add_blank(doc, 8)

    # Место под электронную подпись директора.
    add_text(doc, "Место для подписи: ___________________________", align=RIGHT)
    add_blank(doc)
    add_text(doc, "ФИО: _____________________________________________", align=RIGHT)
    add_blank(doc)
    add_text(doc, "Дата: _________________", align=RIGHT)
    add_blank(doc, 3)

    add_text(doc, "Составитель(и) рабочей программы:", bold=True)
    # Склеиваем через запятую только заполненные поля, чтобы не было «Иванов, ».
    teacher = ", ".join(part for part in (data.teacher_name, data.teacher_title) if part)
    add_text(doc, teacher)
    add_text(doc, "(подпись)                                 (ФИО, ученая степень, звание)")
    add_blank(doc)

    add_text(doc, f"Программа одобрена на заседании кафедры «{data.department}»")
    add_text(doc, f"«____» ______________ {year} г., протокол № ____")
    add_blank(doc)

    add_text(doc, "Программа одобрена на заседании УМС структурного подразделения")
    add_text(doc, f"{data.ums_date}, протокол № {data.ums_protocol}")


def add_table_of_contents(doc: Document, data: RPDGenerateRequest) -> None:
    """Оглавление: название пункта, табуляция, номер страницы."""
    if not data.toc_items:
        return

    doc.add_page_break()
    add_text(doc, "СОДЕРЖАНИЕ", size=14, bold=True, align=CENTER)
    add_blank(doc)

    for item in data.toc_items:
        _add_toc_line(doc, item.title, item.page)
        for subitem in data.toc_subitems.get(item.id, []):
            _add_toc_line(doc, "    " + subitem.title, subitem.page, indented=True)


def _add_toc_line(doc: Document, title: str, page: str, *, indented: bool = False) -> None:
    """Одна строка оглавления. Подчёркивание в имени — знак «функция только для этого файла»."""
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.tab_stops.add_tab_stop(PAGE_NUMBER_TAB)
    if indented:
        paragraph.paragraph_format.left_indent = LIST_INDENT
    style_run(paragraph.add_run(title))
    paragraph.add_run("\t")
    style_run(paragraph.add_run(page))
