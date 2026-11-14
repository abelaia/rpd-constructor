"""Pydantic-модели: описание данных, которые клиент присылает на сервер.

FastAPI сам сверяет входящий JSON с этими моделями. Если данные не подходят
(нет обязательного поля, не тот тип) — клиент получает ответ 422 с описанием
ошибки, а до генерации документа дело не доходит.
"""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TocItem(BaseModel):
    """Пункт оглавления (раздел I–IX)."""

    id: str
    title: str
    page: str


class TocSubitem(BaseModel):
    """Подпункт оглавления (например, 4.1)."""

    title: str
    page: str


class Competence(BaseModel):
    """Строка таблицы компетенций (раздел III)."""

    competence: str
    indicator: str
    results: str


class Table41Row(BaseModel):
    """Строка таблицы 4.1 — содержание дисциплины по темам."""

    num: str = ""
    topic: str = ""
    lectures: str = ""
    practical: str = ""
    laboratory: str = ""
    consultations: str = ""
    independent: str = ""
    format: str = ""
    assessment: str = ""
    control_type: str = ""
    points: str = ""


class Table42Row(BaseModel):
    """Строка таблицы 4.2 — план самостоятельной работы."""

    num: str = ""
    topic: str = ""
    semester: str = ""
    deadline: str = ""
    work_type: str = ""
    hours: str = ""
    materials: str = ""


class TableVIRow(BaseModel):
    """Строка таблицы материально-технического обеспечения (раздел VI)."""

    num: str = ""
    type: str = ""
    audience: str = ""
    equipment: str = ""


class TableVIIIRow(BaseModel):
    """Строка паспорта фонда оценочных средств (раздел VIII)."""

    num: str = ""
    code: str = ""
    name: str = ""


class LabWork(BaseModel):
    """Описание лабораторной работы (раздел VIII)."""

    number: int = 1
    goal: str = ""
    tasks: str = ""
    theory: str = ""
    steps: str = ""
    questions: str = ""


class SectionContents(BaseModel):
    """Наполнение разделов документа. Имена полей совпадают с тем, что шлёт клиент."""

    # noqa: E741 — линтер считает имя «I» неразборчивым, но это ключ из JSON клиента.
    I: str = ""  # noqa: E741
    II: str = ""
    III_desc: str = (
        "Освоение дисциплины направлено на формирование следующих компетенций "
        "в соответствии с образовательным стандартом и образовательной программой:"
    )
    III_competencies: list[Competence] = Field(default_factory=list)
    IV_table: list[Table41Row] = Field(default_factory=list)
    IV_table42: list[Table42Row] = Field(default_factory=list)
    V_main_literature: str = ""
    V_additional_literature: str = ""
    V_internet_resources: str = ""
    VI_description: str = (
        "При реализации дисциплины используются следующие помещения, "
        "оборудование и программное обеспечение:"
    )
    VI_table: list[TableVIRow] = Field(default_factory=list)
    VII: str = ""
    VIII_table: list[TableVIIIRow] = Field(default_factory=list)
    VIII_labs: list[LabWork] = Field(default_factory=list)
    IX: str = ""


class RPDGenerateRequest(BaseModel):
    """Всё, что нужно для генерации одной рабочей программы."""

    # Единственное обязательное поле: без названия документ не имеет смысла.
    discipline_name: str = Field(min_length=1)
    teacher_name: str = ""
    teacher_title: str = ""
    department: str = ""
    ums_date: str = ""
    ums_protocol: str = ""
    credits: int = 5
    total_hours: int = 180
    attestation_form: str = "зачёт"
    custom_filename: str | None = None
    toc_items: list[TocItem] = Field(default_factory=list)
    toc_subitems: dict[str, list[TocSubitem]] = Field(default_factory=dict)
    section_contents: SectionContents = Field(default_factory=SectionContents)


class ProgramSummary(BaseModel):
    """Краткие сведения о сохранённой программе — для списка."""

    # from_attributes разрешает собирать модель прямо из объекта базы данных.
    model_config = ConfigDict(from_attributes=True)

    id: int
    discipline_name: str
    teacher_name: str
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def mark_as_utc(cls, value: datetime) -> datetime:
        """SQLite не хранит часовой пояс, поэтому при чтении явно помечаем время как UTC.

        Тогда в JSON уходит «...Z», и браузер сам переводит время в местное.
        """
        return value if value.tzinfo else value.replace(tzinfo=UTC)


class ProgramDetail(ProgramSummary):
    """Сохранённая программа целиком: сведения из списка плюс всё содержимое."""

    data: RPDGenerateRequest
