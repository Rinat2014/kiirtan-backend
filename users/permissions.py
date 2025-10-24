# users/permissions.py
from rest_framework import permissions


class IsModeratorOrStaff(permissions.BasePermission):
    """
    Разрешает доступ к списку пользователей только модераторам и staff
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_staff or user.groups.filter(name="Moderators").exists()


class CanEditUserGroups(permissions.BasePermission):
    """
    Разрешает изменять группы пользователя только если:
    - пользователь является staff, или
    - состоит в группе 'Moderators'
    """
    def has_permission(self, request, view):
        # Только аутентифицированные могут менять
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # PATCH/PUT/DELETE разрешены только staff или Moderators
        if request.method in ("PATCH", "PUT", "DELETE"):
            return request.user.is_staff or request.user.groups.filter(name="Moderators").exists()
        # Для остальных методов (GET) оставляем стандартное поведение
        return True



from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(BaseUserSerializer):
    # Позволяет менять группы при PATCH/PUT
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("groups",)