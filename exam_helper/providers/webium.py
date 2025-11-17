"""Поставщик заданий из открытого банка заданий оналйн школы webium."""

from exam_helper.models import Task

from .base import BaseProvider

_BASE_URL = "https://bank-zadaniy.webium.ru/api/v2/task-bank/topics/"
_SUBJECT_ID = {
    "география": 1,
    "информатика": 2,
    "биология": 3,
    "профильная математика": 4,
    "русский язык": 5,
    "химия": 6,
    "английския язык": 7,
    "история": 8,
    "физика": 9,
    "литература": 10,
    "обществознание": 11,
    "базовая математика": 13,
}


class WebiumProvider(BaseProvider):
    """Поставщик заданий из открытого банка заданий оналйн школы webium."""

    def task(self, subject: str, kim_id: int) -> list[Task] | None:
        """Получение заданий."""
        if subject not in _SUBJECT_ID:
            print(
                f"Провайдер {self.__class__} не поддерживает предмет: {subject}",
            )
            return None

        subject_id = _SUBJECT_ID[subject]

        with self.session.get(
            f"{_BASE_URL}{subject_id}/tasks",
            params={
                "number_in_kim_id": kim_id,
            },
        ) as r:
            return [
                Task(
                    task["id"],
                    task["description"],
                    task["numberInKim"],
                    [i["name"] for i in task["subThemes"]],
                )
                for task in r.json()
            ]

    def check(self, subject: str, id_: int, answer: str) -> tuple[bool, str]:
        """Проверка решения задачи."""
        if subject not in _SUBJECT_ID:
            print(
                f"Провайдер {self.__class__} не поддерживает предмет: {subject}",
            )
            return None

        subject_id = _SUBJECT_ID[subject]

        with self.session.post(
            f"{_BASE_URL}{subject_id}/tasks/{id_}/add-solution/",
            json={"text": answer},
        ) as r:
            print(r.url)
            data = r.json()
            print(data)
            data = data["correctAnswers"]

        return (
            data["correctAnswer"],
            data["explanation"],
        )

    def kim_numbers(self, subject: str) -> None:
        """Список номеров заданий в КИМ-ах."""
        if subject not in _SUBJECT_ID:
            print(
                f"Провайдер {self.__class__} не поддерживает предмет: {subject}",
            )
            return None

        subject_id = _SUBJECT_ID[subject]

        with self.session.get(
            f"{_BASE_URL}{subject_id}/kim-numbers",
        ) as r:
            return [i["id"] for i in r.json()]
