"""Работа с базой данных."""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt

from exam_helper.models import Task

_DB_FILE = Path("exam_helper.sqlite")


class ExamHelperDB:
    """Работа с базой данных."""

    def __init__(self) -> None:
        """Инициализация базы данных."""
        self.connection = sqlite3.connect(_DB_FILE)
        self.cursor = self.connection.cursor()

    def add_task(self, task: Task, solved: bool) -> None:
        """Добавление записи о решении задачи."""
        # TODO: Добавление информации о задаче
        self.cursor.execute(
            "INSERT INTO tasks (id, solved) VALUES (?, ?)",
            (task.id_, solved),
        )
        self.connection.commit()

    def get_statistics(self) -> None:
        """Получение статистики/аналитики по решеным задачам."""
        self.cursor.execute(
            "SELECT * FROM tasks",
        )
        tasks = self.cursor.fetchall()

        # Генерируем график аналитики
        plt.plot([task[1] for task in tasks])
        plt.savefig("graph.png")


# TODO: Нужно ещё запихать что-то в другую таблицу бд
# (возможно какие-то константы просто из gui.py)
