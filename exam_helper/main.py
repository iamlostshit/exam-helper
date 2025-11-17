"""Запуск приложения."""

import sys

import qdarktheme
from PySide6.QtWidgets import QApplication

from exam_helper.gui import ExamHelperApp


def main() -> None:
    """Запуск приложения."""

    class _QtFallback:
        class AlignmentFlag:
            AlignCenter = 0

    app = QApplication(sys.argv)
    eh = ExamHelperApp()
    qdarktheme.setup_theme()
    eh.show()
    sys.exit(app.exec())
