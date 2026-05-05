# news/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
]

















# from django.urls import path
# from . import views


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import NewsViewSet

# router = DefaultRouter()
# router.register(r'news', NewsViewSet, basename='news')

# urlpatterns = [
#     path('', include(router.urls)),
# ]



# urlpatterns = [
#     path('news/', views.NewsListView.as_view(), name='news-list'),
#     path('news/<int:page>/', views.NewsListView.as_view(), name='news-list-paginated'),
#     path('news/content/<str:identifier>/', views.NewsContentAPIView.as_view(), name='news-content'),
#     path('news/content/create/', views.NewsCreateAPIView.as_view(), name='news-create'),
#     path('news/content/update/<int:pk>/', views.NewsUpdateAPIView.as_view(), name='news-update'),
# ]




















# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import NewsViewSet

# router = DefaultRouter()
# router.register(r'news', NewsViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import NewsViewSet

# router = DefaultRouter()
# router.register(r'news', NewsViewSet, basename='news')

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]

# # Дополнительные URL для получения по slug
# urlpatterns += [
#     path('api/news/by-slug/<slug:slug>/', 
#          NewsViewSet.as_view({'get': 'by_slug'}), 
#          name='news-by-slug'),
# ]





# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r'news', views.NewsViewSet, basename='news')
# router.register(r'news/(?P<news_pk>\d+)/translations', 
#                 views.NewsTranslationViewSet, 
#                 basename='news-translations')

# urlpatterns = [
#     path('', include(router.urls)),
#     # Дополнительные эндпоинты
#     path('news/', views.NewsViewSet.as_view({
#         'get': 'list',
#         'post': 'create'
#     }), name='news-list-create'),
    
#     path('news/latest/', views.NewsViewSet.as_view({
#         'get': 'latest'
#     }), name='news-latest'),
    
#     path('news/page/<int:page_number>/', views.NewsViewSet.as_view({
#         'get': 'page'
#     }), name='news-page'),
    
#     path('news/<slug:slug>/', views.NewsViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'patch': 'partial_update',
#         'delete': 'destroy'
#     }), name='news-detail'),
    
#     path('news_create/', views.NewsViewSet.as_view({
#         'post': 'create'
#     }), name='news-create'),
# ]

# # Для backward compatibility
# urlpatterns += router.urls