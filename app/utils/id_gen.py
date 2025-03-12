import uuid


def generate_uuid_v4_without_special_chars():
    return str(uuid.uuid4()).replace('-', '')
