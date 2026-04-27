from fastapi import FastAPI, Response, Request
from fastapi.responses import FileResponse
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.schemas import RPDGenerateRequest
from docx import Document
import re
from docx.oxml.ns import qn
from datetime import datetime
from unidecode import unidecode
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import RGBColor
from docx.shared import Pt
import io
import os
import uvicorn
import json
import traceback

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def set_font(run, size=None, bold=False, italic=False, font_name='Times New Roman'):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    if size:
        run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)

def sanitize_filename(filename: str, max_length: int = 100) -> str:
    if not filename:
        return "document"

    name, ext = os.path.splitext(filename)

    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '_', name)
    name = name.strip().strip('.')
    name = re.sub(r'[\x00-\x1f\x7f]', '', name)

    if len(name) > max_length:
        name = name[:max_length]

    if not name:
        name = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return name


def generate_default_name(discipline_name: str) -> str:
    base_name = discipline_name.split('(')[0].strip() if '(' in discipline_name else discipline_name
    if not base_name:
        base_name = "program"
    date_str = datetime.now().strftime('%Y%m%d')
    return sanitize_filename(f"RPD_{base_name}_{date_str}")


def prepare_filename(filename: str) -> str:
    clean_name = sanitize_filename(filename)
    translit_name = unidecode(clean_name)
    return f"{translit_name}.docx"


def set_page_orientation(doc, orientation='portrait'):
    section = doc.sections[-1]

    if orientation == 'landscape':
        new_width = section.page_height
        new_height = section.page_width
        section.page_width = new_width
        section.page_height = new_height

        sectPr = section._sectPr
        pgSz = sectPr.find(qn('w:pgSz'))
        if pgSz is None:
            pgSz = OxmlElement('w:pgSz')
            sectPr.append(pgSz)
        pgSz.set(qn('w:orient'), 'landscape')
    else:
        sectPr = section._sectPr
        pgSz = sectPr.find(qn('w:pgSz'))
        if pgSz is not None and pgSz.get(qn('w:orient')) is not None:
            pgSz.set(qn('w:orient'), 'portrait')

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-word")
async def generate_word(request: Request):
    try:
        raw_data = await request.json()

        validated_data = RPDGenerateRequest(**raw_data)

        custom_filename = validated_data.custom_filename or ''
        discipline_name = validated_data.discipline_name
        teacher_name = validated_data.teacher_name
        teacher_title = validated_data.teacher_title
        department = validated_data.department
        ums_date = validated_data.ums_date
        ums_protocol = validated_data.ums_protocol

        toc_items = [item.dict() for item in validated_data.toc_items]
        toc_subitems = {
            k: [sub.dict() for sub in v]
            for k, v in validated_data.toc_subitems.items()
        }
        section_contents = validated_data.section_contents.dict()

        doc = Document()
        style = doc.styles['Normal']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(12)

        for level in range(1, 10):
            heading_style = doc.styles[f'Heading {level}']
            heading_style.font.name = 'Times New Roman'

        para1 = doc.add_paragraph()
        run1 = para1.add_run('МИНОБРНАУКИ РОССИИ')
        set_font(run1, size=10, bold=False)
        para1.alignment = WD_ALIGN_PARAGRAPH.CENTER

        para2 = doc.add_paragraph()
        para2.add_run(
            'Федеральное государственное автономное образовательное\nучреждение высшего образования «Южный федеральный университет»\n(ЮЖНЫЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ)')
        for run in para2.runs:
            set_font(run, size=12, bold=False)
        para2.alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_paragraph()
        doc.add_paragraph()
        doc.add_paragraph()
        doc.add_paragraph()
        doc.add_paragraph()

        para3 = doc.add_paragraph()
        run3 = para3.add_run('РАБОЧАЯ ПРОГРАММА ДИСЦИПЛИНЫ (МОДУЛЯ)')
        set_font(run3, size=14, bold=True)
        para3.alignment = WD_ALIGN_PARAGRAPH.CENTER

        para4 = doc.add_paragraph()
        run4 = para4.add_run(discipline_name)
        set_font(run4, size=14, bold=False)
        para4.alignment = WD_ALIGN_PARAGRAPH.CENTER

        for _ in range(7):
            doc.add_paragraph()

        doc.add_paragraph()
        signature_line = doc.add_paragraph()
        signature_line.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_sig = signature_line.add_run('Место для подписи: ___________________________')
        set_font(run_sig, size=12, bold=False)

        doc.add_paragraph()
        fio_line = doc.add_paragraph()
        fio_line.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_fio = fio_line.add_run('ФИО: _____________________________________________')
        set_font(run_fio, size=12, bold=False)

        doc.add_paragraph()
        date_line = doc.add_paragraph()
        date_line.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_date = date_line.add_run('Дата: _________________')
        set_font(run_date, size=12, bold=False)

        for _ in range(3):
            doc.add_paragraph()

        para9 = doc.add_paragraph()
        run9 = para9.add_run('Составитель(и) рабочей программы:')
        set_font(run9, size=12, bold=True)

        teacher_info = f'{teacher_name}, {teacher_title}'
        para10 = doc.add_paragraph()
        run10 = para10.add_run(teacher_info)
        set_font(run10, size=12, bold=False)

        p_sub = doc.add_paragraph('(подпись)                                 (ФИО, ученая степень, звание)')
        run_sub = p_sub.runs[0]
        set_font(run_sub, size=12, bold=False)

        doc.add_paragraph()
        para11 = doc.add_paragraph()
        run11_1 = para11.add_run('Программа одобрена на заседании кафедры «')
        set_font(run11_1, size=12, bold=False)
        run11_2 = para11.add_run(department)
        set_font(run11_2, size=12, bold=False)
        run11_3 = para11.add_run('»')
        set_font(run11_3, size=12, bold=False)

        doc.add_paragraph('«____» ______________ 2025 г., протокол № ____')
        run_protocol = doc.paragraphs[-1].runs[0]
        set_font(run_protocol, size=12, bold=False)

        doc.add_paragraph()
        para12 = doc.add_paragraph()
        run12 = para12.add_run('Программа одобрена на заседании УМС структурного подразделения')
        set_font(run12, size=12, bold=False)

        doc.add_paragraph(f'{ums_date}, протокол № {ums_protocol}')
        run_last = doc.paragraphs[-1].runs[0]
        set_font(run_last, size=12, bold=False)

        if toc_items:
            doc.add_page_break()

            title = doc.add_paragraph()
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = title.add_run('СОДЕРЖАНИЕ')
            set_font(run, size=14, bold=True)

            doc.add_paragraph()

            for item in toc_items:
                p = doc.add_paragraph()
                p.paragraph_format.tab_stops.add_tab_stop(Pt(450))

                title_text = item.get('title', '')
                page_text = item.get('page', '')

                run_title = p.add_run(title_text)
                set_font(run_title, size=12, bold=False)

                p.add_run('\t')

                page_run = p.add_run(page_text)
                set_font(page_run, size=12, bold=False)
                page_run.font.color.rgb = RGBColor(0, 0, 0)

                item_id = item.get('id', '')
                subitems = toc_subitems.get(item_id, [])

                for subitem in subitems:
                    p2 = doc.add_paragraph()
                    p2.paragraph_format.left_indent = Pt(36)
                    p2.paragraph_format.tab_stops.add_tab_stop(Pt(450))

                    sub_title = subitem.get('title', '')
                    sub_page = subitem.get('page', '')

                    run_sub_title = p2.add_run('    ' + sub_title)
                    set_font(run_sub_title, size=12, bold=False)

                    p2.add_run('\t')
                    subpage_run = p2.add_run(sub_page)
                    set_font(subpage_run, size=12, bold=False)
                    subpage_run.font.color.rgb = RGBColor(0, 0, 0)
        else:
            print("Нет пунктов содержания")

        doc.add_page_break()

        heading1 = doc.add_heading('I. ЦЕЛИ И ЗАДАЧИ ОСВОЕНИЯ ДИСЦИПЛИНЫ', 1)
        heading1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading1.runs:
            set_font(run, size=14, bold=True)
        doc.add_paragraph()

        section1_text = section_contents.get('I', '')
        if section1_text:
            lines = section1_text.strip().split('\n')
            for line in lines:
                if line.strip():
                    if line.strip().startswith('-'):
                        p = doc.add_paragraph(line.strip().replace('-', '•'), style='List Bullet')
                    else:
                        p = doc.add_paragraph(line.strip())
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            doc.add_paragraph('Текст раздела не введен.')
            for run in p.runs:
                set_font(run, size=12, bold=False)

        doc.add_page_break()

        heading2 = doc.add_heading('II. МЕСТО ДИСЦИПЛИНЫ В СТРУКТУРЕ ОБРАЗОВАТЕЛЬНОЙ ПРОГРАММЫ', 1)
        heading2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading2.runs:
            set_font(run, size=14, bold=True)
        doc.add_paragraph()

        section2_text = section_contents.get('II', '')
        if section2_text:
            lines = section2_text.strip().split('\n')
            for line in lines:
                if line.strip():
                    if line.strip().startswith('-'):
                        p = doc.add_paragraph(line.strip().replace('-', '•'), style='List Bullet')
                    else:
                        p = doc.add_paragraph(line.strip())
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            doc.add_paragraph('Текст раздела не введен.')
            for run in p.runs:
                set_font(run, size=12, bold=False)

        doc.add_page_break()
        doc.add_section()
        set_page_orientation(doc, 'landscape')

        heading3 = doc.add_heading('III. ТРЕБОВАНИЯ К РЕЗУЛЬТАТАМ ОСВОЕНИЯ ДИСЦИПЛИНЫ', 1)
        heading3.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading3.runs:
            set_font(run, size=14, bold=True)
        doc.add_paragraph()

        section3_desc = section_contents.get('III_desc',
                                             'Освоение дисциплины направлено на формирование следующих компетенций в соответствии с образовательным стандартом и образовательной программой:')
        p_desc = doc.add_paragraph(section3_desc)
        for run in p_desc.runs:
            set_font(run, size=12, bold=False)
        doc.add_paragraph()

        table_title = doc.add_paragraph(
            'Перечень планируемых результатов обучения по дисциплине, соотнесённых с индикаторами достижения компетенций')
        table_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in table_title.runs:
            set_font(run, size=12, bold=True)
        doc.add_paragraph()

        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'

        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Компетенция'
        hdr_cells[1].text = 'Индикаторы достижения компетенции'
        hdr_cells[2].text = 'Результаты обучения'
        for cell in hdr_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    set_font(run, size=12, bold=True)

        competencies = section_contents.get('III_competencies', [])

        if competencies:
            for comp in competencies:
                row_cells = table.add_row().cells
                row_cells[0].text = comp.get('competence', '')
                row_cells[1].text = comp.get('indicator', '')
                row_cells[2].text = comp.get('results', '')
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)
        else:
            row_cells = table.add_row().cells
            row_cells[0].text = 'ОПК-1. Способен решать актуальные задачи фундаментальной и прикладной математики'
            row_cells[1].text = 'ОПК-3.1. Решает актуальные задачи фундаментальной и прикладной математики'
            row_cells[
                2].text = 'Знания:\n– Решения актуальных задач фундаментальной и прикладной математики\n\nУмения:\n– Решать актуальные задачи фундаментальной и прикладной математики\n\nНавыки:\n– Решения актуальные задачи фундаментальной и прикладной математики'
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        set_font(run, size=12, bold=False)
        doc.add_page_break()

        heading4 = doc.add_heading('IV. СОДЕРЖАНИЕ И СТРУКТУРА ДИСЦИПЛИНЫ', 1)
        heading4.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading4.runs:
            set_font(run, size=14, bold=True)
        doc.add_paragraph()

        credits = validated_data.credits
        total_hours = validated_data.total_hours
        attestation_form = validated_data.attestation_form

        p_credits = doc.add_paragraph(f'Трудоёмкость дисциплины составляет {credits} зачётных единиц, {total_hours} часов,')
        for run in p_credits.runs:
            set_font(run, size=12, bold=False)
        p_attest = doc.add_paragraph(f'Форма промежуточной аттестации: {attestation_form}')
        for run in p_attest.runs:
            set_font(run, size=12, bold=False)
        doc.add_paragraph()

        heading4_1 = doc.add_heading(
            '4.1. Содержание дисциплины, структурированное по темам (учебным встречам) для 1 семестра очной формы обучения',
            2)
        for run in heading4_1.runs:
            set_font(run, size=12, bold=True)
            run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()
        table_data = section_contents.get('IV_table', [])
        table = doc.add_table(rows=1, cols=11)
        table.style = 'Table Grid'

        headers = [
            '№ п/п',
            'Тема занятия и рассматриваемые вопросы',
            'Лекции',
            'Практические',
            'Лабораторные',
            'Консультации',
            'Самостоятельная работа',
            'Формат проведения занятия',
            'Наименование оценочного средства',
            'Вид контроля',
            'Сумма баллов за занятие'
        ]

        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header
            for run in hdr_cells[i].paragraphs[0].runs:
                set_font(run, size=12, bold=False)

        default_rows = []
        if table_data:
            for row_data in table_data:
                row_cells = table.add_row().cells
                row_cells[0].text = str(row_data.get('num', ''))
                row_cells[1].text = row_data.get('topic', '')
                row_cells[2].text = str(row_data.get('lectures', ''))
                row_cells[3].text = str(row_data.get('practical', ''))
                row_cells[4].text = str(row_data.get('laboratory', ''))
                row_cells[5].text = str(row_data.get('consultations', ''))
                row_cells[6].text = str(row_data.get('independent', ''))
                row_cells[7].text = row_data.get('format', '')
                row_cells[8].text = row_data.get('assessment', '')
                row_cells[9].text = row_data.get('control_type', '')
                row_cells[10].text = str(row_data.get('points', ''))
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)
        else:
            default_rows = [
                {'num': '1', 'topic': 'Тема 1. Фреймворк Spring 5', 'lectures': '2', 'practical': '-',
                 'laboratory': '-', 'consultations': '-', 'independent': '8', 'format': 'Информационная лекция',
                 'assessment': '-', 'control_type': '-', 'points': '-'},
                {'num': '2', 'topic': 'Тема 1. Фреймворк Spring 5', 'lectures': '-', 'practical': '2',
                 'laboratory': '-', 'consultations': '-', 'independent': '-',
                 'format': 'Репродуктивная лабораторная работа', 'assessment': 'лабораторная работа № 1',
                 'control_type': 'подготовка и сдача отчёта по лабораторной работе', 'points': '5'},
                {'num': '3', 'topic': 'Тема 2. Введение в Spring Boot', 'lectures': '2', 'practical': '-',
                 'laboratory': '-', 'consultations': '-', 'independent': '-', 'format': 'Информационная лекция',
                 'assessment': '-', 'control_type': '-', 'points': '-'},
                {'num': '4', 'topic': 'Тема 2. Введение в Spring Boot', 'lectures': '-', 'practical': '2',
                 'laboratory': '-', 'consultations': '-', 'independent': '-',
                 'format': 'Репродуктивная лабораторная работа', 'assessment': 'лабораторная работа № 2',
                 'control_type': 'подготовка и сдача отчёта по лабораторной работе', 'points': '5'},
                {'num': '5', 'topic': 'Тема 3. Внутреннее устройство и возможности Spring Boot', 'lectures': '2',
                 'practical': '-', 'laboratory': '-', 'consultations': '-', 'independent': '-',
                 'format': 'Информационная лекция', 'assessment': '-', 'control_type': '-', 'points': '-'},
                {'num': '6', 'topic': 'Тема 3. Внутреннее устройство и возможности Spring Boot', 'lectures': '-',
                 'practical': '2', 'laboratory': '-', 'consultations': '-', 'independent': '-',
                 'format': 'Репродуктивная лабораторная работа', 'assessment': 'лабораторная работа № 3',
                 'control_type': 'подготовка и сдача отчёта по лабораторной работе', 'points': '6'},
                {'num': '7', 'topic': 'Тема 4. Создание веб-приложений', 'lectures': '3', 'practical': '-',
                 'laboratory': '-', 'consultations': '-', 'independent': '-', 'format': 'Информационная лекция',
                 'assessment': '-', 'control_type': '-', 'points': '-'},
            ]
            for row_data in default_rows:
                row_cells = table.add_row().cells
                row_cells[0].text = row_data['num']
                row_cells[1].text = row_data['topic']
                row_cells[2].text = row_data['lectures']
                row_cells[3].text = row_data['practical']
                row_cells[4].text = row_data['laboratory']
                row_cells[5].text = row_data['consultations']
                row_cells[6].text = row_data['independent']
                row_cells[7].text = row_data['format']
                row_cells[8].text = row_data['assessment']
                row_cells[9].text = row_data['control_type']
                row_cells[10].text = row_data['points']
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)

        if table_data or default_rows:
            total_row = table.add_row()
            total_cells = total_row.cells
            total_cells[0].merge(total_cells[9])
            run_total = total_cells[0].paragraphs[0].add_run('Итого часов')
            set_font(run_total, size=12, bold=True)

            total_lectures = 0
            total_laboratory = 0
            total_independent = 0
            total_points = 0
            rows_to_sum = table_data if table_data else default_rows

            for row in rows_to_sum:
                try:
                    total_lectures += int(row.get('lectures', '0')) if str(row.get('lectures', '0')).isdigit() else 0
                except:
                    pass
                try:
                    total_laboratory += int(row.get('laboratory', '0')) if str(row.get('laboratory', '0')).isdigit() else 0
                except:
                    pass
                try:
                    total_independent += int(row.get('independent', '0')) if str(row.get('independent', '0')).isdigit() else 0
                except:
                    pass
                try:
                    points_val = str(row.get('points', '0')).replace('-', '0')
                    total_points += int(points_val) if points_val.isdigit() else 0
                except:
                    pass
            total_cells[10].text = str(total_points)
            total_cells[2].text = str(total_lectures)
            total_cells[4].text = str(total_laboratory)
            total_cells[6].text = str(total_independent)
            for cell in [total_cells[2], total_cells[4], total_cells[6], total_cells[10]]:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        set_font(run, size=12, bold=True)

        doc.add_paragraph()

        heading4_2 = doc.add_heading('4.2. План внеаудиторной самостоятельной работы', 2)
        for run in heading4_2.runs:
            set_font(run, size=12, bold=True)
            run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()
        table42_data = section_contents.get('IV_table42', [])
        table42 = doc.add_table(rows=1, cols=7)
        table42.style = 'Table Grid'

        headers42 = [
            '№ п/п',
            'Тема занятия',
            'Семестр',
            'Сроки выполнения (нед.)',
            'Вид самостоятельной работы',
            'Затраты времени (часы)',
            'Учебно-методическое обеспечение'
        ]

        hdr_cells42 = table42.rows[0].cells
        for i, header in enumerate(headers42):
            hdr_cells42[i].text = header
            for run in hdr_cells42[i].paragraphs[0].runs:
                set_font(run, size=12, bold=False)

        total_hours_sum = 0

        if table42_data:

            for row_data in table42_data:
                row_cells = table42.add_row().cells
                row_cells[0].text = str(row_data.get('num', ''))
                row_cells[1].text = row_data.get('topic', '')
                row_cells[2].text = str(row_data.get('semester', ''))
                row_cells[3].text = str(row_data.get('deadline', ''))
                row_cells[4].text = row_data.get('work_type', '')
                hours = str(row_data.get('hours', '0'))
                row_cells[5].text = hours
                row_cells[6].text = row_data.get('materials', '')
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)
                try:
                    total_hours_sum += int(hours) if hours.isdigit() else 0
                except:
                    pass
        else:
            default_rows42 = [
                {'num': '1', 'topic': 'Тема 1. Фреймворк Spring 5', 'semester': '1', 'deadline': '1',
                 'work_type': '- проработка и повторение материала лекционных занятий;\n- подготовка к лабораторной работе',
                 'hours': '8', 'materials': '-'},
                {'num': '2', 'topic': 'Тема 2. Введение в Spring Boot', 'semester': '1', 'deadline': '2',
                 'work_type': '- проработка и повторение материала лекционных занятий;\n- подготовка к лабораторной работе',
                 'hours': '8', 'materials': '-'},
                {'num': '3', 'topic': 'Тема 3. Внутреннее устройство и возможности Spring Boot',
                 'semester': '1', 'deadline': '3',
                 'work_type': '- проработка и повторение материала лекционных занятий;\n- подготовка к лабораторной работе',
                 'hours': '8', 'materials': '-'},
                {'num': '4', 'topic': 'Тема 4. Создание веб-приложений', 'semester': '1', 'deadline': '4',
                 'work_type': '- проработка и повторение материала лекционных занятий;\n- подготовка к лабораторной работе',
                 'hours': '8', 'materials': '-'},
            ]
            for row_data in default_rows42:
                row_cells = table42.add_row().cells
                row_cells[0].text = row_data['num']
                row_cells[1].text = row_data['topic']
                row_cells[2].text = row_data['semester']
                row_cells[3].text = row_data['deadline']
                row_cells[4].text = row_data['work_type']
                row_cells[5].text = row_data['hours']
                row_cells[6].text = row_data['materials']
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)
                try:
                    total_hours_sum += int(row_data['hours']) if row_data['hours'].isdigit() else 0
                except:
                    pass

        total_row = table42.add_row()
        total_cells = total_row.cells
        total_cells[0].merge(total_cells[4])
        run_total42 = total_cells[0].paragraphs[0].add_run('Общая трудоёмкость самостоятельной работы по дисциплине')
        set_font(run_total42, size=12, bold=True)
        total_cells[5].text = str(total_hours_sum)
        for run in total_cells[5].paragraphs[0].runs:
            set_font(run, size=12, bold=True)
        total_cells[6].text = ''

        doc.add_page_break()
        doc.add_section()
        set_page_orientation(doc, 'portrait')

        heading5 = doc.add_heading('V. УЧЕБНО-МЕТОДИЧЕСКОЕ ОБЕСПЕЧЕНИЕ ДИСЦИПЛИНЫ', 1)
        heading5.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading5.runs:
            set_font(run, size=14, bold=True)
        heading5.style.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()

        heading5_1 = doc.add_heading('5.1. Основная литература', 2)
        for run in heading5_1.runs:
            set_font(run, size=12, bold=True)
            run.font.color.rgb = RGBColor(0, 0, 0)

        main_lit = section_contents.get('V_main_literature', '')
        if main_lit:
            lines = main_lit.strip().split('\n')
            for line in lines:
                if line.strip():
                    p = doc.add_paragraph(line.strip())
                    p.paragraph_format.left_indent = Pt(36)
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            p = doc.add_paragraph('Список основной литературы не введен.')
            p.paragraph_format.left_indent = Pt(36)
            for run in p.runs:
                set_font(run, size=12, bold=False)

        doc.add_paragraph()
        heading5_2 = doc.add_heading('5.2. Дополнительная литература', 2)
        for run in heading5_2.runs:
            set_font(run, size=12, bold=True)
            run.font.color.rgb = RGBColor(0, 0, 0)

        additional_lit = section_contents.get('V_additional_literature', '')
        if additional_lit:
            lines = additional_lit.strip().split('\n')
            for line in lines:
                if line.strip():
                    p = doc.add_paragraph(line.strip())
                    p.paragraph_format.left_indent = Pt(36)
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            p = doc.add_paragraph('Список дополнительной литературы не введен.')
            p.paragraph_format.left_indent = Pt(36)
            for run in p.runs:
                set_font(run, size=12, bold=False)

        doc.add_paragraph()
        heading5_3 = doc.add_heading('5.3. Перечень ресурсов сети Интернет', 2)
        for run in heading5_3.runs:
            set_font(run, size=12, bold=True)
            run.font.color.rgb = RGBColor(0, 0, 0)

        internet_res = section_contents.get('V_internet_resources', '')
        if internet_res:
            lines = internet_res.strip().split('\n')
            for line in lines:
                if line.strip():
                    p = doc.add_paragraph(line.strip())
                    p.paragraph_format.left_indent = Pt(36)
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            p = doc.add_paragraph('Список интернет-ресурсов не введен.')
            p.paragraph_format.left_indent = Pt(36)
            for run in p.runs:
                set_font(run, size=12, bold=False)

        doc.add_page_break()

        heading6 = doc.add_heading('VI. МАТЕРИАЛЬНО-ТЕХНИЧЕСКОЕ ОБЕСПЕЧЕНИЕ ДИСЦИПЛИНЫ', 1)
        heading6.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading6.runs:
            set_font(run, size=14, bold=True)
        heading6.style.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()

        vi_description = section_contents.get('VI_description', 'При реализации дисциплины используются следующие помещения, оборудование и программное обеспечение:')
        doc.add_paragraph(vi_description)
        for run in p_desc.runs:
            set_font(run, size=12, bold=False)
        doc.add_paragraph()
        table_vi_data = section_contents.get('VI_table', [])

        if table_vi_data:
            table_vi = doc.add_table(rows=1, cols=4)
            table_vi.style = 'Table Grid'

            headers_vi = ['№ п/п', 'Тип аудиторного занятия', 'Рекомендуемая аудитория', 'Оснащение']
            hdr_cells_vi = table_vi.rows[0].cells
            for i, header in enumerate(headers_vi):
                hdr_cells_vi[i].text = header
                for run in hdr_cells_vi[i].paragraphs[0].runs:
                    set_font(run, size=12, bold=False)

            for row_data in table_vi_data:
                row_cells = table_vi.add_row().cells
                row_cells[0].text = str(row_data.get('num', ''))
                row_cells[1].text = row_data.get('type', '')
                row_cells[2].text = row_data.get('audience', '')
                row_cells[3].text = row_data.get('equipment', '')
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)
        doc.add_page_break()

        heading7 = doc.add_heading('VII. МЕТОДИЧЕСКИЕ УКАЗАНИЯ ДЛЯ ОБУЧАЮЩИХСЯ ПО ОСВОЕНИЮ ДИСЦИПЛИНЫ', 1)
        heading7.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading7.runs:
            set_font(run, size=14, bold=True)
        heading7.style.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()

        section7_text = section_contents.get('VII', '')
        if section7_text:
            lines = section7_text.strip().split('\n')
            for line in lines:
                if line.strip():
                    p = doc.add_paragraph(line.strip())
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            doc.add_paragraph('Методические указания не введены.')
            for run in p.runs:
                set_font(run, size=12, bold=False)

        doc.add_page_break()

        heading8 = doc.add_heading('VIII. ФОНД ОЦЕНОЧНЫХ СРЕДСТВ', 1)
        heading8.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading8.runs:
            set_font(run, size=14, bold=True)
        heading8.style.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()

        heading8_1 = doc.add_heading('8.1. Паспорт фонда оценочных средств', 2)
        for run in heading8_1.runs:
            set_font(run, size=12, bold=True)
        doc.add_paragraph()

        table_viii_data = section_contents.get('VIII_table', [])
        if table_viii_data:
            table_viii = doc.add_table(rows=1, cols=3)
            table_viii.style = 'Table Grid'
            headers_viii = ['№ п/п', 'Код индикатора достижения компетенции', 'Наименование оценочного средства']
            hdr_cells_viii = table_viii.rows[0].cells
            for i, header in enumerate(headers_viii):
                hdr_cells_viii[i].text = header
                for run in hdr_cells_viii[i].paragraphs[0].runs:
                    set_font(run, size=12, bold=False)
            for row_data in table_viii_data:
                row_cells = table_viii.add_row().cells
                row_cells[0].text = str(row_data.get('num', ''))
                row_cells[1].text = row_data.get('code', '')
                row_cells[2].text = row_data.get('name', '')
                for cell in row_cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            set_font(run, size=12, bold=False)

        # 8.2. Лабораторные работы
        doc.add_paragraph()
        heading8_2 = doc.add_heading('8.2. Лабораторные работы', 2)
        for run in heading8_2.runs:
            set_font(run, size=12, bold=True)
        doc.add_paragraph()

        labs_data = section_contents.get('VIII_labs', [])
        for lab in labs_data:
            lab_title = doc.add_heading(f'Лабораторная работа №{lab.get("number", 1)}', 3)
            for run in lab_title.runs:
                set_font(run, size=12, bold=True)

            if lab.get('goal'):
                p = doc.add_paragraph()
                run_goal = p.add_run('Цель работы: ')
                set_font(run_goal, size=12, bold=True)
                run_goal_text = p.add_run(lab.get('goal'))
                set_font(run_goal_text, size=12, bold=False)
            if lab.get('tasks'):
                p = doc.add_paragraph()
                run_tasks = p.add_run('Задачи: ')
                set_font(run_tasks, size=12, bold=True)
                run_tasks_text = p.add_run(lab.get('tasks'))
                set_font(run_tasks_text, size=12, bold=False)
            if lab.get('theory'):
                p = doc.add_paragraph()
                run_theory = p.add_run('Теоретические сведения: ')
                set_font(run_theory, size=12, bold=True)
                run_theory_text = p.add_run(lab.get('theory'))
                set_font(run_theory_text, size=12, bold=False)
            if lab.get('steps'):
                p = doc.add_paragraph()
                run_steps = p.add_run('Порядок выполнения: ')
                set_font(run_steps, size=12, bold=True)
                lines = lab.get('steps').split('\n')
                for line in lines:
                    if line.strip():
                        p_step = doc.add_paragraph(line.strip(), style='List Number')
                        for run in p_step.runs:
                            set_font(run, size=12, bold=False)
            if lab.get('questions'):
                p = doc.add_paragraph()
                run_questions = p.add_run('Контрольные вопросы: ')
                set_font(run_questions, size=12, bold=True)
                lines = lab.get('questions').split('\n')
                for line in lines:
                    if line.strip():
                        p_q = doc.add_paragraph(line.strip(), style='List Bullet')
                        for run in p_q.runs:
                            set_font(run, size=12, bold=False)
            doc.add_paragraph()

        doc.add_page_break()

        heading9 = doc.add_heading('IX. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ', 1)
        heading9.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in heading9.runs:
            set_font(run, size=14, bold=True)
        heading9.style.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph()

        section9_text = section_contents.get('IX', '')
        if section9_text:
            lines = section9_text.strip().split('\n')
            for line in lines:
                if line.strip():
                    p = doc.add_paragraph(line.strip())
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        set_font(run, size=12, bold=False)
        else:
            doc.add_paragraph('Дополнительная информация не указана.')
            for run in p.runs:
                set_font(run, size=12, bold=False)

        # Сохраняем документ
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        if custom_filename:
            safe_filename = prepare_filename(custom_filename)
        else:
            base_name = generate_default_name(discipline_name)
            safe_filename = prepare_filename(base_name)

        return Response(
            content=file_stream.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=\"{safe_filename}\""
            }
        )

    except Exception as e:
        print(f"ОШИБКА при создании документа: {e}")
        print("Полный traceback:")
        traceback.print_exc()

        return Response(
            content=json.dumps({"error": str(e)}),
            media_type="application/json",
            status_code=500
        )


if __name__ == "__main__":
    print("Откройте: http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
