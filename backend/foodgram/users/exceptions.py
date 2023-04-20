from rest_framework.exceptions import ValidationError


class WrongData(ValidationError):
    """400 ошибка при не корректных данных."""
    ...


class CantSubscribe(ValidationError):
    """400 ошибка при повторной подписке и подписке на себя."""
    ...
