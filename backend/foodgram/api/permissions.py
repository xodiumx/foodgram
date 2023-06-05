from recipes.models import Recipe
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request


class IsAuthorAndAuthenticatedOrReadOnly(BasePermission):
    """
    Изменять чужие записи запрещено.
    И не аутентифицированный пользователь может воспользоваться методами из:
    SAFE_METHODS
    """
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request: Request, _) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(
            self,
            request: Request,
            _, obj: Recipe) -> bool:
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
