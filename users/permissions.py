from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "Ошибка! Вы не являетесь автором!"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
