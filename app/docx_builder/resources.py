"""Разделы V (литература) и VI (материально-техническое обеспечение)."""

from docx.document import Document

from app.schemas import SectionContents

from .helpers import LIST_INDENT, add_blank, add_heading, add_table, add_text, add_text_block

HEADERS_VI = ("№ п/п", "Тип аудиторного занятия", "Рекомендуемая аудитория", "Оснащение")


def add_literature(doc: Document, contents: SectionContents) -> None:
    """Раздел V. Учебно-методическое обеспечение."""
    add_heading(doc, "V. УЧЕБНО-МЕТОДИЧЕСКОЕ ОБЕСПЕЧЕНИЕ ДИСЦИПЛИНЫ")
    add_blank(doc)

    # Три подраздела устроены одинаково, поэтому описываем их списком
    # (заголовок, текст, заглушка) и выводим в цикле.
    subsections = (
        (
            "5.1. Основная литература",
            contents.V_main_literature,
            "Список основной литературы не введен.",
        ),
        (
            "5.2. Дополнительная литература",
            contents.V_additional_literature,
            "Список дополнительной литературы не введен.",
        ),
        (
            "5.3. Перечень ресурсов сети Интернет",
            contents.V_internet_resources,
            "Список интернет-ресурсов не введен.",
        ),
    )
    for index, (title, text, placeholder) in enumerate(subsections):
        if index > 0:
            add_blank(doc)
        add_heading(doc, title, level=2)
        add_text_block(doc, text, placeholder=placeholder, indent=LIST_INDENT)


def add_facilities(doc: Document, contents: SectionContents) -> None:
    """Раздел VI. Материально-техническое обеспечение."""
    add_heading(doc, "VI. МАТЕРИАЛЬНО-ТЕХНИЧЕСКОЕ ОБЕСПЕЧЕНИЕ ДИСЦИПЛИНЫ")
    add_blank(doc)
    add_text(doc, contents.VI_description)
    add_blank(doc)

    if contents.VI_table:
        rows = [(r.num, r.type, r.audience, r.equipment) for r in contents.VI_table]
        add_table(doc, HEADERS_VI, rows)
