import re


def is_valid_phone(phone: str) -> bool:
    """
    Провряет валидность номера телефона
    """
    pattern = r'^(?:\+375|375)\d{9}$'
    try:
        if re.match(pattern, phone):
            return True
    except TypeError:
        pass
    return False


def is_valid_name(name: str) -> bool:
    """
    Проверяет валидность имени
    """
    try:
        if not name.isalpha() or len(name) < 2:
            return False
    except (TypeError, AttributeError):
        return False
    return True
