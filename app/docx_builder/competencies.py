"""Раздел III. Требования к результатам освоения дисциплины."""

from docx.document import Document

from app.schemas import SectionContents

from .helpers import CENTER, add_blank, add_heading, add_table, add_text

HEADERS = ("Компетенция", "Индикаторы достижения компетенции", "Результаты обучения")


def add_competencies(doc: Document, contents: SectionContents) -> None:
    add_heading(doc, "III. ТРЕБОВАНИЯ К РЕЗУЛЬТАТАМ ОСВОЕНИЯ ДИСЦИПЛИНЫ")
    add_blank(doc)
    add_text(doc, contents.III_desc)
    add_blank(doc)
    add_text(
        doc,
        "Перечень планируемых результатов обучения по дисциплине, "
        "соотнесённых с индикаторами достижения компетенций",
        bold=True,
        align=CENTER,
    )
    add_blank(doc)

    rows = [(c.competence, c.indicator, c.results) for c in contents.III_competencies]
    add_table(doc, HEADERS, rows, bold_header=True)
