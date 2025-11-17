"""Конфигурация и инициализация некторых данных."""

from exam_helper.db import ExamHelperDB
from exam_helper.providers import WebiumProvider
from exam_helper.providers.webium import _SUBJECT_ID

supported_subjects = list(_SUBJECT_ID.keys())
#               ^^^^^^^^^^^
# TODO: На данный момент реализован только один провайдер =>
# TODO: Один список предметов => используется приватная константа.

parser = WebiumProvider()
parser.init()

db = ExamHelperDB()
