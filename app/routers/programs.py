"""API сохранённых рабочих программ.

Адреса построены по правилам REST: один ресурс — «программа» (/api/programs),
а действие над ним определяется HTTP-методом:

  GET    /api/programs           список
  POST   /api/programs           создать
  GET    /api/programs/{id}      получить одну
  PUT    /api/programs/{id}      заменить содержимое
  DELETE /api/programs/{id}      удалить
  GET    /api/programs/{id}/docx скачать документ
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.docx_builder import build_rpd
from app.filenames import build_filename
from app.models import Program
from app.schemas import ProgramDetail, ProgramSummary, RPDGenerateRequest

logger = logging.getLogger("rpd.programs")

DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# APIRouter — «мини-приложение» с группой маршрутов; main.py подключает его целиком.
router = APIRouter(prefix="/api/programs", tags=["Программы"])

# Сокращение: «параметр session, который FastAPI получает из get_session».
SessionDep = Annotated[Session, Depends(get_session)]


def docx_response(data: RPDGenerateRequest) -> Response:
    """Собирает документ и оборачивает его в HTTP-ответ со скачиванием файла."""
    try:
        content = build_rpd(data)
    except Exception as error:
        # Подробности пишем в журнал сервера, пользователю — короткое сообщение.
        logger.exception("Не удалось сформировать документ «%s»", data.discipline_name)
        raise HTTPException(status_code=500, detail="Не удалось сформировать документ") from error

    filename = build_filename(data.custom_filename, data.discipline_name)
    return Response(
        content=content,
        media_type=DOCX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def get_program_or_404(session: Session, program_id: int) -> Program:
    """Ищет программу по номеру; если её нет — отвечает ошибкой 404."""
    program = session.get(Program, program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    return program


def fill_program(program: Program, data: RPDGenerateRequest) -> None:
    """Переносит данные формы в объект базы данных."""
    program.discipline_name = data.discipline_name
    program.teacher_name = data.teacher_name
    program.data = data.model_dump()


@router.get("")
def list_programs(session: SessionDep) -> list[ProgramSummary]:
    """Список программ: недавно изменённые — сверху."""
    query = select(Program).order_by(Program.updated_at.desc(), Program.id.desc())
    return [ProgramSummary.model_validate(program) for program in session.scalars(query)]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_program(data: RPDGenerateRequest, session: SessionDep) -> ProgramSummary:
    program = Program()
    fill_program(program, data)
    session.add(program)
    session.commit()
    logger.info("Сохранена программа №%s «%s»", program.id, program.discipline_name)
    return ProgramSummary.model_validate(program)


@router.get("/{program_id}")
def get_program(program_id: int, session: SessionDep) -> ProgramDetail:
    return ProgramDetail.model_validate(get_program_or_404(session, program_id))


@router.put("/{program_id}")
def update_program(
    program_id: int, data: RPDGenerateRequest, session: SessionDep
) -> ProgramSummary:
    program = get_program_or_404(session, program_id)
    fill_program(program, data)
    session.commit()
    return ProgramSummary.model_validate(program)


@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(program_id: int, session: SessionDep) -> None:
    session.delete(get_program_or_404(session, program_id))
    session.commit()


@router.get("/{program_id}/docx")
def download_program(program_id: int, session: SessionDep) -> Response:
    """Формирует .docx из сохранённых данных."""
    program = get_program_or_404(session, program_id)
    return docx_response(RPDGenerateRequest.model_validate(program.data))
