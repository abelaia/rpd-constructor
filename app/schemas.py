# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TocItem(BaseModel):
    id: str
    title: str
    page: str

class TocSubitem(BaseModel):
    title: str
    page: str

class Competence(BaseModel):
    competence: str
    indicator: str
    results: str

class Table41Row(BaseModel):
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
    num: str = ""
    topic: str = ""
    semester: str = ""
    deadline: str = ""
    work_type: str = ""
    hours: str = ""
    materials: str = ""

class LiteratureItem(BaseModel):
    number: str = ""
    authors: str = ""
    title: str = ""
    edition: str = ""
    city: str = ""
    publisher: str = ""
    year: str = ""
    pages: str = ""
    isbn: str = ""

class TableVIRow(BaseModel):
    num: str = ""
    type: str = ""
    audience: str = ""
    equipment: str = ""

class TableVIIIRow(BaseModel):
    num: str = ""
    code: str = ""
    name: str = ""

class LabWork(BaseModel):
    number: int = 1
    goal: str = ""
    tasks: str = ""
    theory: str = ""
    steps: str = ""
    questions: str = ""

class InternetResource(BaseModel):
    number: str = ""
    title: str = ""
    resource_type: str = ""
    url: str = ""
    access_date: str = ""

class SectionContents(BaseModel):
    I: Optional[str] = ""
    II: Optional[str] = ""
    III_desc: Optional[str] = ""
    III_competencies: List[Competence] = Field(default_factory=list)
    IV_credits: int = 5
    IV_hours: int = 180
    IV_attestation: str = "зачёт"
    IV_table: List[Table41Row] = Field(default_factory=list)
    IV_table42: List[Table42Row] = Field(default_factory=list)
    V_main_literature: str = ""
    V_additional_literature: str = ""
    V_internet_resources: str = ""
    VI_description: str = "При реализации дисциплины используются следующие помещения, оборудование и программное обеспечение:"
    VI_table: List[TableVIRow] = Field(default_factory=list)
    VII: Optional[str] = ""
    VIII_table: List[TableVIIIRow] = Field(default_factory=list)
    VIII_labs: List[LabWork] = Field(default_factory=list)
    IX: Optional[str] = ""

class RPDGenerateRequest(BaseModel):
    discipline_name: str = "Basics of SpringBoot (Основы SpringBoot)"
    teacher_name: str = "О. Ю. Кравченко"
    teacher_title: str = "к. ф.-м.н., доцент"
    department: str = "Технологии автоматизации в бизнесе"
    ums_date: str = "«22» апреля 2025 г."
    ums_protocol: str = "4"
    credits: int = 5
    total_hours: int = 180
    attestation_form: str = "зачёт"
    custom_filename: Optional[str] = None
    toc_items: List[TocItem] = Field(default_factory=list)
    toc_subitems: Dict[str, List[TocSubitem]] = Field(default_factory=dict)
    section_contents: SectionContents = Field(default_factory=SectionContents)

    class Config:
        json_schema_extra = {
            "example": {
                "discipline_name": "Basics of SpringBoot (Основы SpringBoot)",
                "teacher_name": "О. Ю. Кравченко",
                "teacher_title": "к. ф.-м.н., доцент",
                "department": "Технологии автоматизации в бизнесе",
                "ums_date": "«22» апреля 2025 г.",
                "ums_protocol": "4",
                "credits": 5,
                "total_hours": 180,
                "attestation_form": "зачёт",
                "custom_filename": "Моя_программа",
                "toc_items": [
                    {"id": "I", "title": "I. Цели и задачи освоения дисциплины", "page": "4"},
                    {"id": "II", "title": "II. Место дисциплины в структуре ОП", "page": "4"}
                ],
                "toc_subitems": {
                    "IV": [
                        {"title": "4.1. Содержание дисциплины...", "page": "6"}
                    ]
                },
                "section_contents": {
                    "I": "Цели: ...",
                    "II": "Место: ...",
                    "III_desc": "Освоение дисциплины направлено на...",
                    "III_competencies": [{"competence": "ОПК-1", "indicator": "ОПК-1.1", "results": "знания"}],
                    "IV_credits": 5,
                    "IV_hours": 180,
                    "IV_attestation": "зачёт",
                    "IV_table": [],
                    "IV_table42": [],
                    "V_main_literature": "1. Уоллс, К. Spring в действии...",
                    "V_additional_literature": "",
                    "V_internet_resources": "",
                    "VI_description": "При реализации дисциплины используются...",
                    "VI_table": [],
                    "VII": "Методические указания...",
                    "VIII_table": [],
                    "VIII_labs": [],
                    "IX": "Зачёт выставляется, если...",
                }
            }
        }

class RPDGenerateResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    error: Optional[str] = None
