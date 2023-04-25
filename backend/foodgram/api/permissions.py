from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorAndAuthenticatedOrReadOnly(BasePermission):
    """
    Изменять чужие записи запрещено.
    И не аутентифицированный пользователь может воспользоваться методами из:
    SAFE_METHODS
    """
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
