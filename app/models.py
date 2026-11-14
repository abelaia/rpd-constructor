"""Модели — описание таблиц базы данных в виде классов Python."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _now() -> datetime:
    """Текущее время в UTC: в базе храним единое время, а не время конкретного компьютера."""
    return datetime.now(UTC)


class Program(Base):
    """Сохранённая рабочая программа дисциплины — одна строка таблицы programs.

    Содержимое программы целиком лежит в столбце data в формате JSON — в том же
    виде, в каком его присылает форма. Название и составитель продублированы
    в отдельных столбцах, чтобы показывать список программ, не разбирая JSON.

    Пока форма активно меняется, так проще: новое поле формы не требует менять
    таблицу. Когда структура устоится, данные можно будет разложить по
    отдельным таблицам (компетенции, темы, литература).
    """

    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True)
    discipline_name: Mapped[str] = mapped_column(String(500), index=True)
    teacher_name: Mapped[str] = mapped_column(String(200), default="")
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now
    )
