"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/users/', include('users.urls')),
#     path('api/', include('news.urls')),
#     path('api/', include('musicians.urls')),
#     path('api/', include('moderators.urls')),
# ]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import GroupListView
from users.views import (
  MusiciansListView,
  ModeratorMusiciansListView,
  )

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/', include('news.urls')),
    path('api/', include('musicians.urls')),
    path('api/', include('moderators.urls')),

    path('api/users/musicians/', MusiciansListView.as_view(), name='musicians-list'),
    path('api/users/moderators/', ModeratorMusiciansListView.as_view(), name='moderators'),

    path("api/groups/", GroupListView.as_view(), name="group-list"),

    
    
    # DJOSER
    
    path('api/auth/', include('djoser.urls')),
    # POST /auth/users/ — регистрация пользователя
    # GET /auth/users/ — список пользователей (если разрешено)
    # GET /auth/users/{id}/ — получить данные пользователя по ID
    # DELETE /auth/users/{id}/ — удалить пользователя
    # PUT /auth/users/{id}/ — полное обновление пользователя
    # PATCH /auth/users/{id}/ — частичное обновление пользователя
    # GET /auth/users/me/ — текущий пользователь
    # PUT /auth/users/me/ — обновить текущего пользователя
    # PATCH /auth/users/me/ — частично обновить текущего пользователя
    # DELETE /auth/users/me/ — удалить текущего пользователя
    # POST /auth/users/resend_activation/ — повторно отправить письмо активации
    # POST /auth/users/set_password/ — сменить пароль (если знаешь текущий)
    # POST /auth/users/reset_password/ — запрос на сброс пароля (письмо)
    # POST /auth/users/reset_password_confirm/ — подтверждение сброса пароля
    # POST /auth/users/set_username/ — сменить username
    # POST /auth/users/reset_username/ — запрос на сброс username
    # POST /auth/users/reset_username_confirm/ — подтверждение сброса username

    path('api/auth/', include('djoser.urls.jwt')),  
    # POST /auth/jwt/create/ — получить access + refresh токены
    # POST /auth/jwt/refresh/ — обновить access токен
    # POST /auth/jwt/verify/ — проверить токен

    # Стандартные токены
    # path('auth/', include('djoser.urls.authtoken')),
    # POST /auth/token/login/ — получить токен (по username/email + пароль)
    # POST /auth/token/logout/ — удалить токен





    # эндпоинты:
    # POST /auth/users/ — регистрация
    # POST /auth/jwt/create/ — получить access+refresh токены
    # POST /auth/jwt/refresh/ — обновить access
    # GET  /auth/users/me/ — текущий пользователь
    # POST /auth/users/activation/ — активация аккаунта (по ссылке из письма)
    # POST /auth/users/resend_activation/ — повторная отправка
    # POST /auth/users/reset_password/ — запрос на сброс пароля
    # POST /auth/users/reset_password_confirm/ — подтверждение сброса

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






# DJoser эндпоинты по умолчанию --- включаются в зависимости от того, что ты добавил в urls.py

# POST   /auth/users/                  # регистрация пользователя
# GET    /auth/users/                  # список пользователей (если разрешено)
# GET    /auth/users/{id}/             # получить данные пользователя по ID (если разрешено)
# DELETE /auth/users/{id}/             # удалить пользователя (если разрешено)
# PUT    /auth/users/{id}/             # полное обновление пользователя (если разрешено)
# PATCH  /auth/users/{id}/             # частичное обновление пользователя (если разрешено)

# GET    /auth/users/me/               # текущий пользователь
# PUT    /auth/users/me/               # обновить текущего пользователя
# PATCH  /auth/users/me/               # частично обновить текущего пользователя
# DELETE /auth/users/me/               # удалить текущего пользователя

# POST   /auth/users/resend_activation/ # повторно отправить письмо активации
# POST   /auth/users/set_password/      # сменить пароль (если знаешь текущий)
# POST   /auth/users/reset_password/    # запрос на сброс пароля (письмо)
# POST   /auth/users/reset_password_confirm/ # подтверждение сброса пароля
# POST   /auth/users/set_username/      # сменить username
# POST   /auth/users/reset_username/    # запрос на сброс username
# POST   /auth/users/reset_username_confirm/ # подтверждение сброса username