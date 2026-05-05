from rest_framework import permissions

class IsModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешает обновлять и удалять только модераторам и админам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or
            request.user.groups.filter(name='Moderators').exists()
        )