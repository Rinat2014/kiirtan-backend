from rest_framework import permissions

class IsMusicianOrHigher(permissions.BasePermission):
    """
    Разрешает добавлять только музыкантам и админам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or
            request.user.groups.filter(name='Musicians').exists()
            # request.user.groups.filter(name='Moderators').exists()
        )

class IsModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешает обновлять и удалять только модераторам и админам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or
            request.user.groups.filter(name='Moderators').exists()
        )

class IsMusicianOwnerOrModerator(permissions.BasePermission):
    """
    Разрешает удалять запись музыканту (если это его запись) или модератору.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user == obj.musician or 
            request.user.is_staff or
            request.user.groups.filter(name='Moderators').exists()
        )

# class IsMusician(permissions.BasePermission):
#     """
#     Разрешение только для пользователей с ролью музыканта
#     """
#     def has_permission(self, request, view):
#         # return request.user.is_authenticated and request.user.role == 'musician'
#         return request.user.is_authenticated and (
#             request.user.is_staff or
#             request.user.groups.filter(name='Musicians').exists()
#             # request.user.groups.filter(name='Moderators').exists()
#         )