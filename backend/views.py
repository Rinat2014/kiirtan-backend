from django.contrib.auth.models import Group
from rest_framework import generics
from users.serializers import GroupSerializer
from users.permissions import IsModeratorOrStaff

class GroupListView(generics.ListAPIView):
    """
    GET /auth/groups/ -> список всех групп
    Доступ: только staff или Moderators
    """
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [IsModeratorOrStaff]
