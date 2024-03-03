from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь модератором
        return request.user.groups.filter(name='moders').exists()
