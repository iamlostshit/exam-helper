"""Некоторые типы объектов."""

from dataclasses import dataclass


@dataclass
class Task:
    """Объект задания."""

    id_: int
    description: str
    number_in_kim: int
    sub_themes: list[str]
