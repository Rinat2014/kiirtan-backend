# moderators/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModeratorSlotViewSet

router = DefaultRouter()
router.register(r'moderator-slots', ModeratorSlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]