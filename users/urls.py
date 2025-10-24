# users/urls.py
from django.urls import path
from .views import RegisterView, activate_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
  UserMeView,
  CustomTokenObtainPairView,
  MusiciansListView,
  ModeratorMusiciansListView,
  AllActiveUsersView,
  UserInfoView,
  UserInfoUpdateView,
  UserRoleUpdateView,
  )

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('activate/<uuid:user_id>/', activate_user, name='activate-user'),
    # path('login/', TokenObtainPairView.as_view(), name='login'),              # old
    
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # path('me/', TokenObtainPairView.as_view(), name='me')                     # old
    
    path('update/', UserInfoUpdateView.as_view(), name='update'),               # user update data
    path('roles/update/', UserRoleUpdateView.as_view(), name='user-role-update'),
    # path('<int:user_id>/roles/update/', UserRoleUpdateView.as_view(), name='user-role-update'),
    
    path('me/', UserMeView.as_view(), name='me'),
    path('info/', UserInfoView.as_view(), name='info'),
    path('musicians/', MusiciansListView.as_view(), name='musicians-list'),
    path('moderators/', ModeratorMusiciansListView.as_view(), name='moderators'),
    path('', AllActiveUsersView.as_view(), name='all-active-users'),
]
