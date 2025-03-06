from uuid import UUID

def check_uuid(string: str) -> bool:
    try:
        uuid = UUID(string)
        return True

    except Exception:
        return False