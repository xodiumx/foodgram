from rest_framework.exceptions import ValidationError


class UserIsNotAuth(ValidationError):
    """400 ошибка для не аутентифицированного пользователя."""
    ...
