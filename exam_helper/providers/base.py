"""Базовый поставщик заданий."""

from abc import ABC, abstractmethod

import requests

from exam_helper.models import Task


class BaseProvider(ABC):
    """Базовый поставщик заданий.

    Занимется поставкой заданий в формае ОГЭ/ЕГЭ из некоторого источника.
    """

    def init(self) -> None:
        """Инициализация сессии для парсинга."""
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json"},
        )

    @abstractmethod
    def task(self, subject: str, num: int) -> list[Task] | None:
        """Получение заданий."""

    @abstractmethod
    def check(self, subject: str, id_: int, answer: str) -> tuple[bool, str]:
        """Получение решений."""
