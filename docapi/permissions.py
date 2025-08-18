from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Проверка прав доступа для администратора.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Проверка прав доступа для владельца объекта или администратора.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
