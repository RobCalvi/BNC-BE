from enum import Enum


class ReminderState(str, Enum):
    NOT_PAST = "NOT_PAST"
    PAST = "PAST"
