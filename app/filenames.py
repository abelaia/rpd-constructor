"""Формирование безопасного имени файла для скачивания."""

import os
import re
from datetime import datetime

from unidecode import unidecode

# Символы, запрещённые в именах файлов Windows.
_INVALID_CHARS = re.compile(r'[<>:"/\\|?*]')
# Невидимые управляющие символы.
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """Убирает из имени расширение и все символы, недопустимые в имени файла."""
    name, _extension = os.path.splitext(filename or "")
    name = _INVALID_CHARS.sub("_", name)
    name = _CONTROL_CHARS.sub("", name)
    name = name.strip().strip(".")[:max_length]
    return name or f"document_{datetime.now():%Y%m%d_%H%M%S}"


def default_name(discipline_name: str) -> str:
    """Имя по умолчанию: «RPD_<название до скобки>_<дата>»."""
    base_name = discipline_name.split("(")[0].strip() or "program"
    return f"RPD_{base_name}_{datetime.now():%Y%m%d}"


def build_filename(custom_filename: str | None, discipline_name: str) -> str:
    """Возвращает итоговое имя .docx-файла латиницей.

    Имя уходит в HTTP-заголовок Content-Disposition, а заголовки должны быть
    в ASCII, поэтому кириллицу переводим в латиницу библиотекой unidecode.
    """
    name = sanitize_filename(custom_filename or default_name(discipline_name))
    return f"{unidecode(name)}.docx"
