from enum import Enum


class OperationType(str, Enum):
    """
     Action Operation Types
    """
    CALL = "CALL"
    EMAIL = "EMAIL"
    ONLINE_MEETING = "ONLINE_MEETING"
    IN_PERSON_MEETING = "IN_PERSON_MEETING"


class LogType(str, Enum):
    """
        Change log types
    """
    CREATE_ACTION = "CREATE_ACTION"
    DELETE_ACTION = "DELETE_ACTION"
    UPDATE_DETAIL = "UPDATE_DETAIL"
    CREATE_CONTACT = "CREATE_CONTACT"
    DELETE_CONTACT = "DELETE_CONTACT"
    UPDATE_CONTACT = "UPDATE_CONTACT"
    IMPORT_COMPANIES = "IMPORT_COMPANIES"
