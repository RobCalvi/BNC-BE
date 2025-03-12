from typing import Optional, Any

def safe_float(value: Optional[Any]) -> Optional[float]:
    """
    Function to safely convert to a float.
    :param value: Any value
    :return: flaot or none
    """
    try:
        if value in [None, '']:
            return None
        return float(value)
    except (ValueError, TypeError):
        return None
