"""Раздел IV. Содержание и структура дисциплины (таблицы 4.1 и 4.2)."""

from docx.document import Document
from docx.table import Table

from app.schemas import RPDGenerateRequest, Table41Row, Table42Row

from .helpers import add_blank, add_heading, add_table, add_text, set_cell_text, style_run, to_int

HEADERS_41 = (
    "№ п/п",
    "Тема занятия и рассматриваемые вопросы",
    "Лекции",
    "Практические",
    "Лабораторные",
    "Консультации",
    "Самостоятельная работа",
    "Формат проведения занятия",
    "Наименование оценочного средства",
    "Вид контроля",
    "Сумма баллов за занятие",
)

HEADERS_42 = (
    "№ п/п",
    "Тема занятия",
    "Семестр",
    "Сроки выполнения (нед.)",
    "Вид самостоятельной работы",
    "Затраты времени (часы)",
    "Учебно-методическое обеспечение",
)


def add_structure(doc: Document, data: RPDGenerateRequest) -> None:
    contents = data.section_contents

    add_heading(doc, "IV. СОДЕРЖАНИЕ И СТРУКТУРА ДИСЦИПЛИНЫ")
    add_blank(doc)
    add_text(
        doc,
        f"Трудоёмкость дисциплины составляет {data.credits} зачётных единиц, "
        f"{data.total_hours} часов,",
    )
    add_text(doc, f"Форма промежуточной аттестации: {data.attestation_form}")
    add_blank(doc)

    add_heading(
        doc,
        "4.1. Содержание дисциплины, структурированное по темам (учебным встречам) "
        "для 1 семестра очной формы обучения",
        level=2,
    )
    add_blank(doc)
    _add_table_41(doc, contents.IV_table)
    add_blank(doc)

    add_heading(doc, "4.2. План внеаудиторной самостоятельной работы", level=2)
    add_blank(doc)
    _add_table_42(doc, contents.IV_table42)


def _add_table_41(doc: Document, rows: list[Table41Row]) -> None:
    table = add_table(
        doc,
        HEADERS_41,
        [
            (
                r.num,
                r.topic,
                r.lectures,
                r.practical,
                r.laboratory,
                r.consultations,
                r.independent,
                r.format,
                r.assessment,
                r.control_type,
                r.points,
            )
            for r in rows
        ],
    )
    if not rows:
        return

    # Итоговая строка: суммы по каждому столбцу с часами и по баллам.
    totals = {
        2: sum(to_int(r.lectures) for r in rows),
        3: sum(to_int(r.practical) for r in rows),
        4: sum(to_int(r.laboratory) for r in rows),
        5: sum(to_int(r.consultations) for r in rows),
        6: sum(to_int(r.independent) for r in rows),
        10: sum(to_int(r.points) for r in rows),
    }
    _add_total_row(table, "Итого", label_span=2, totals=totals)


def _add_table_42(doc: Document, rows: list[Table42Row]) -> None:
    table = add_table(
        doc,
        HEADERS_42,
        [(r.num, r.topic, r.semester, r.deadline, r.work_type, r.hours, r.materials) for r in rows],
    )
    if not rows:
        return

    _add_total_row(
        table,
        "Общая трудоёмкость самостоятельной работы по дисциплине",
        label_span=5,
        totals={5: sum(to_int(r.hours) for r in rows)},
    )


def _add_total_row(table: Table, label: str, *, label_span: int, totals: dict[int, int]) -> None:
    """Добавляет жирную итоговую строку.

    label_span — сколько первых ячеек объединить под подпись;
    totals — «номер столбца → сумма» (столбцы считаются с нуля).
    """
    cells = table.add_row().cells
    # Сначала пишем числа, потом объединяем ячейки: после объединения
    # старые ссылки на ячейки перестают работать.
    for column, total in totals.items():
        set_cell_text(cells[column], str(total), bold=True)
    merged = cells[0].merge(cells[label_span - 1])
    style_run(merged.paragraphs[0].add_run(label), bold=True)
