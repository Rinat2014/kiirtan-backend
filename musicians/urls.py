# musicians/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MusicSlotViewSet #, MyScheduleViewSet

router = DefaultRouter()
router.register(r'music-slots', MusicSlotViewSet)
# router.register(r'my-schedule-kiirtans', MyScheduleViewSet, basename='my-schedule')

urlpatterns = [
    path('', include(router.urls)),
]
