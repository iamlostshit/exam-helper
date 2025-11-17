"""Организация GUI и запуск приложения на PyQt (без HTML)."""

from random import choice

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from exam_helper.config import db, parser, supported_subjects
from exam_helper.models import Task

_WIDTH = 1000
_HEIGHT = 500


def get_random_task(subject: str) -> Task:
    """Получение случайного задания."""
    return choice(parser.task(subject, choice(parser.kim_numbers(subject))))


class ExamHelperApp(QMainWindow):
    """Главное окно приложения."""

    def __init__(self) -> None:
        """Инициализация приложения."""
        super().__init__()
        self.setWindowTitle("exam-helper")
        self.setGeometry(500, 500, _WIDTH, _HEIGHT)

        # По умолчанию выбрана информатика
        self.choice_subject(0)

    def choice_subject(self, subject: str) -> None:
        """Выбор предмета для проверки знаний."""
        self.subject = supported_subjects[subject]
        self.task_screen()

    def check_answer(self) -> None:
        """Функция для проверки ответа пользователя."""
        user_answer = self.answer_input.text()
        answer, explanation = parser.check(
            "информатика",
            self.task.id_,
            user_answer,
        )

        if answer == user_answer:
            self.result_label.setText("Ответ верный!")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText(f"Ответ неверный, {answer}. {explanation}")
            self.result_label.setStyleSheet("color: red;")

        # Добавляем отчёт в бд
        db.add_task(answer == user_answer)
        self.answer_input.clear()

    def task_screen(self) -> None:
        """Экран решения задач (заготовка)."""
        # Кнопка просмотра аналитики
        analytics_button = QPushButton("Аналитика")
        analytics_button.clicked.connect(self.statistics_screen)

        # Кнопка пропуска задачи
        next_button = QPushButton("Пропуск / следующая задача")
        next_button.clicked.connect(self.choice_subject)

        # Меню выбора предмета
        combo = QComboBox(self)
        combo.addItems(supported_subjects)
        combo.activated.connect(self.choice_subject)

        # Возьмём случайное задание
        self.task = get_random_task(self.subject)

        # Описание
        description = QLabel(
            f"<h1>Задание №{self.task.number_in_kim}</h1>"
            f"{self.task.description}"
            f"Используемые темы: {''.join(self.task.sub_themes)}",
        )
        description.setScaledContents(True)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px;")

        description.setTextInteractionFlags(
            Qt.TextSelectableByMouse
            | Qt.TextSelectableByKeyboard
            | Qt.LinksAccessibleByMouse,
        )

        # Поле для ввода ответа
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Введите ваш ответ здесь...")

        # Кнопка проверки ответа
        check_button = QPushButton("Проверить ответ")
        check_button.clicked.connect(self.check_answer)

        # Метка для отображения результата проверки
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 14px;")
        self.result_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
            | Qt.TextSelectableByKeyboard
            | Qt.LinksAccessibleByMouse,
        )

        # Оформление
        central = QWidget(self)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # Компоновка
        root_layout.addWidget(next_button)
        root_layout.addWidget(combo)
        root_layout.addWidget(description)
        root_layout.addSpacing(8)
        root_layout.addWidget(self.answer_input)
        root_layout.addWidget(check_button)
        root_layout.addWidget(self.result_label)
        root_layout.addSpacing(8)

        self.setCentralWidget(central)

    def statistics_screen(self) -> None:
        """Экран аналитики."""
        # Генерируем график
        db.get_statistics()

        # Изображение графика
        graph_image = QLabel()
        graph_image.setPixmap(QPixmap("graph.png"))

        # Кнопка "назад"
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.task_screen)

        # Оформление
        central = QWidget(self)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # Компоновка
        root_layout.addWidget(back_button)
        root_layout.addWidget(graph_image)
        root_layout.addSpacing(8)

        self.setCentralWidget(central)
