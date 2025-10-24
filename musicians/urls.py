# musicians/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MusicSlotViewSet

router = DefaultRouter()
router.register(r'music-slots', MusicSlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
