"""Общие «кирпичики» для сборки документа.

Раньше каждая строчка документа создавалась вручную: add_paragraph, потом
цикл по runs, потом set_font — и так 165 раз. Здесь эти повторы собраны
в несколько функций, а разделы документа просто вызывают их.

Немного терминов библиотеки python-docx:
  Document  — весь документ;
  Paragraph — абзац;
  Run       — кусок текста внутри абзаца с одинаковым оформлением
              (шрифт, размер, жирность задаются именно у Run).
"""

from collections.abc import Iterable, Sequence

from docx.document import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.text.run import Run

FONT_NAME = "Times New Roman"
BASE_SIZE = 12
HEADING_SIZES = {1: 14}  # заголовки остальных уровней — базового размера
LIST_INDENT = Pt(36)
BLACK = RGBColor(0, 0, 0)

CENTER = WD_ALIGN_PARAGRAPH.CENTER
LEFT = WD_ALIGN_PARAGRAPH.LEFT
RIGHT = WD_ALIGN_PARAGRAPH.RIGHT


def setup_styles(doc: Document) -> None:
    """Задаёт шрифт по умолчанию для всего документа."""
    normal = doc.styles["Normal"]
    normal.font.name = FONT_NAME
    normal.font.size = Pt(BASE_SIZE)
    for level in range(1, 10):
        doc.styles[f"Heading {level}"].font.name = FONT_NAME


def style_run(run: Run, *, size: int = BASE_SIZE, bold: bool = False) -> None:
    """Оформляет кусок текста: Times New Roman, чёрный, нужный размер."""
    run.font.name = FONT_NAME
    # Отдельная настройка для кириллицы: без неё Word может подставить другой шрифт.
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = BLACK


def add_text(
    doc: Document,
    text: str,
    *,
    size: int = BASE_SIZE,
    bold: bool = False,
    align: WD_ALIGN_PARAGRAPH | None = None,
    indent: Pt | None = None,
    style: str | None = None,
) -> Paragraph:
    """Добавляет абзац с текстом и сразу его оформляет."""
    paragraph = doc.add_paragraph(style=style)
    style_run(paragraph.add_run(text), size=size, bold=bold)
    if align is not None:
        paragraph.alignment = align
    if indent is not None:
        paragraph.paragraph_format.left_indent = indent
    return paragraph


def add_labeled_text(doc: Document, label: str, text: str = "") -> Paragraph:
    """Абзац вида «Цель работы: текст», где подпись выделена жирным."""
    paragraph = doc.add_paragraph()
    style_run(paragraph.add_run(label), bold=True)
    if text:
        style_run(paragraph.add_run(text))
    return paragraph


def add_blank(doc: Document, count: int = 1) -> None:
    """Добавляет пустые абзацы — так в документе делаются отступы по вертикали."""
    for _ in range(count):
        doc.add_paragraph()


def add_heading(doc: Document, text: str, level: int = 1) -> Paragraph:
    """Заголовок раздела (level=1) или подраздела (level=2, 3)."""
    heading = doc.add_heading(text, level)
    heading.alignment = LEFT
    for run in heading.runs:
        style_run(run, size=HEADING_SIZES.get(level, BASE_SIZE), bold=True)
    return heading


def split_lines(text: str) -> list[str]:
    """Делит текст из поля ввода на непустые строки без пробелов по краям."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def add_text_block(
    doc: Document,
    text: str,
    *,
    placeholder: str,
    bullets: bool = False,
    indent: Pt | None = None,
) -> None:
    """Выводит многострочный текст: каждая строка — отдельный абзац.

    Если текста нет, выводится placeholder («Текст раздела не введен.»).
    При bullets=True строки, начинающиеся с дефиса, становятся пунктами
    маркированного списка. Дефис убирается только в начале строки,
    поэтому слова вроде «веб-приложение» остаются нетронутыми.
    """
    lines = split_lines(text)
    if not lines:
        add_text(doc, placeholder, indent=indent)
        return

    for line in lines:
        if bullets and line.startswith("-"):
            add_text(doc, line.lstrip("-").strip(), style="List Bullet", align=LEFT)
        else:
            add_text(doc, line, align=LEFT, indent=indent)


def set_cell_text(cell: _Cell, text: str, *, bold: bool = False) -> None:
    """Записывает текст в ячейку таблицы и оформляет его."""
    cell.text = text
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            style_run(run, bold=bold)


def add_table(
    doc: Document,
    headers: Sequence[str],
    rows: Iterable[Sequence[str]],
    *,
    bold_header: bool = False,
) -> Table:
    """Создаёт таблицу с рамками: строка заголовков и строки с данными."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"

    for cell, header in zip(table.rows[0].cells, headers, strict=True):
        set_cell_text(cell, header, bold=bold_header)

    for row in rows:
        for cell, value in zip(table.add_row().cells, row, strict=True):
            set_cell_text(cell, value)
    return table


def add_section(doc: Document, *, landscape: bool) -> None:
    """Начинает новую часть документа (с новой страницы) с нужной ориентацией.

    В Word ориентация — свойство не страницы, а «раздела» (section). Новый
    раздел копирует размеры предыдущего, поэтому при смене ориентации ширину
    и высоту нужно поменять местами.
    """
    section = doc.add_section()
    is_landscape = section.page_width > section.page_height
    if is_landscape != landscape:
        section.page_width, section.page_height = section.page_height, section.page_width
    section.orientation = WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT


def to_int(value: str) -> int:
    """Превращает текст ячейки в число; всё, что не число («-», пусто), считается нулём."""
    value = value.strip()
    return int(value) if value.isdigit() else 0
