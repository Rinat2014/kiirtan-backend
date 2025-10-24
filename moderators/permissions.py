from rest_framework import permissions

class IsModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешает обновлять и удалять только модераторам и админам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            # request.user.is_moderator_musicians or 
            # request.user.is_moderator_site or 
            # request.user.is_admin or 
            request.user.is_staff or
            request.user.groups.filter(name='Moderators').exists()
        )