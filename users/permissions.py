from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    """
    Доступ разрешён только владельцу объекта или администратору.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "admin"
            or obj == request.user
            or getattr(obj, "author", None) == request.user
        )
