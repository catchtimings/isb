from enum import Enum

DEFAULT_DIRECTORY = "C:/Users/ct/PycharmProjects/isb/lab4/data"
CARD_NUMBER_DIRECTORY="card_number.json"


class IconTypes(Enum):
    Critical = "critical",
    Warning = "warning",
    Question = "question",
    Information = "information",
    NoIcon = ""