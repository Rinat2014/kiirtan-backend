# from rest_framework import permissions

# class IsStaffOrModeratorOrAuthor(permissions.BasePermission):
#     """
#     Разрешает изменение/удаление, если:
#       - пользователь is_staff, или
#       - состоит в группе 'Editors', или
#       - он автор записи.
#     Просмотр/листинг — доступен всем/аутентифицированным (вьюха решает).
#     """

#     def has_object_permission(self, request, view, obj):
#         # безопасные методы разрешаем (GET, HEAD, OPTIONS)
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         user = request.user
#         if not user or not user.is_authenticated:
#             return False

#         if user.is_staff:
#             return True

#         if user.groups.filter(name="Editors").exists():
#             return True

#         # # автор может редактировать/удалять свою новость
#         # if getattr(obj, "author", None) and obj.author_id == user.id:
#         #     return True

#         return False
