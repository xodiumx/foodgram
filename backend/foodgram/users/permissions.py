from rest_framework.permissions import IsAdminUser, IsAuthenticated


class SuperUserOrAdmin(IsAdminUser):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)
                    )


class UserIsAuthenticated(IsAuthenticated):
    ...
