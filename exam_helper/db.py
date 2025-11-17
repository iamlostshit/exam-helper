"""Работа с базой данных."""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt

_DB_FILE = Path("exam_helper.sqlite")


class ExamHelperDB:
    """Работа с базой данных."""

    def __init__(self) -> None:
        """Инициализация базы данных."""
        self.connection = sqlite3.connect(_DB_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks (solved BOOLEAN)",
        )

    def add_task(self, solved: bool) -> None:
        """Добавление записи о решении задачи."""
        self.cursor.execute(
            "INSERT INTO tasks (solved) VALUES (?)",
            (solved),
        )
        self.connection.commit()

    def get_statistics(self) -> None:
        """Получение статистики/аналитики по решеным задачам."""
        self.cursor.execute(
            "SELECT * FROM tasks",
        )

        # Генерируем график аналитики
        plt.plot(self.cursor.fetchall())
        plt.savefig("graph.png")


# TODO: Нужно ещё запихать что-то в другую таблицу бд
# (возможно какие-то константы просто из gui.py)
