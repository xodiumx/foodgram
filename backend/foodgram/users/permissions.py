from rest_framework.permissions import IsAuthenticated


class UserIsAuthenticated(IsAuthenticated):
    """Доступ для аутентифицированных пользователей."""
    ...
