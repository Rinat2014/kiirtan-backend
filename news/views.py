# news/view.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import News, NewsTranslation
from .serializers import NewsListSerializer, NewsDetailSerializer
from .pagination import NewsPagination

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для новостей"""
    queryset = News.objects.filter(is_published=True)
    pagination_class = NewsPagination
    lookup_field = 'slug'  # Используем slug для детального просмотра
    
    def get_serializer_context(self):
        """Добавляем язык в контекст сериализатора"""
        context = super().get_serializer_context()
        # Получаем язык из параметра запроса или заголовка
        language = self.request.GET.get('lang', 'en')
        context['language'] = language
        return context
    
    def get_queryset(self):
        """Фильтрация по языку (если нужно)"""
        queryset = super().get_queryset()
        
        # Фильтрация по поиску (если понадобится)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(translations__title__icontains=search) |
                Q(translations__content__icontains=search)
            ).distinct()
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Список новостей с пагинацией"""
        page = self.paginate_queryset(self.get_queryset())
        
        if page is not None:
            serializer = NewsListSerializer(
                page, 
                many=True, 
                context={'request': request, 'language': request.GET.get('lang', 'en')}
            )
            return self.get_paginated_response(serializer.data)
        
        serializer = NewsListSerializer(
            self.get_queryset(), 
            many=True, 
            context={'request': request, 'language': request.GET.get('lang', 'en')}
        )
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Получение детальной информации о новости по slug"""
        instance = self.get_object()
        serializer = NewsDetailSerializer(
            instance, 
            context={'request': request, 'language': request.GET.get('lang', 'en')}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='content/(?P<identifier>[^/.]+)')
    def get_by_identifier(self, request, identifier=None):
        """
        Получение новости по ID или slug
        Примеры:
        - /api/news/content/1/ (по ID)
        - /api/news/content/some-slug/ (по slug)
        """
        try:
            # Пробуем найти по ID
            if identifier.isdigit():
                news = get_object_or_404(News, id=int(identifier), is_published=True)
            else:
                # Ищем по slug
                news = get_object_or_404(News, slug=identifier, is_published=True)
        except (ValueError, News.DoesNotExist):
            return Response(
                {'detail': 'News not found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = NewsDetailSerializer(
            news, 
            context={'request': request, 'language': request.GET.get('lang', 'en')}
        )
        return Response(serializer.data)










































# from rest_framework import viewsets, filters, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import News, NewsTranslation
# from .serializers import NewsSerializer
# from .filters import NewsFilter

# class NewsViewSet(viewsets.ModelViewSet):
#     queryset = News.objects.filter(is_published=True)
#     serializer_class = NewsSerializer
#     lookup_field = 'slug'
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = NewsFilter  # Если используете django-filter
#     search_fields = ['translations__title', 'translations__content']
#     ordering_fields = ['published_at', 'author']
#     ordering = ['-published_at']
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Фильтрация по языку через query param
#         lang = self.request.query_params.get('lang', 'en')
        
#         # Можно добавить дополнительную фильтрацию или аннотацию
#         return queryset
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context
    
#     @action(detail=True, methods=['get'])
#     def by_language(self, request, slug=None):
#         """
#         Получение конкретной новости с определенным языком
#         Пример: /api/news/my-news-slug/by_language/?lang=ru
#         """
#         news = get_object_or_404(News, slug=slug, is_published=True)
#         lang = request.query_params.get('lang', 'en')
        
#         try:
#             translation = news.translations.get(language=lang)
#             data = {
#                 'id': news.id,
#                 'author': news.author,
#                 'published_at': news.published_at,
#                 'image': news.image,
#                 'slug': news.slug,
#                 'translation': {
#                     'language': translation.language,
#                     'title': translation.title,
#                     'content': translation.content,
#                     'short_description': translation.short_description
#                 }
#             }
#             return Response(data)
#         except NewsTranslation.DoesNotExist:
#             # Возвращаем английскую версию как fallback
#             try:
#                 translation = news.translations.get(language='en')
#                 data = {
#                     'id': news.id,
#                     'author': news.author,
#                     'published_at': news.published_at,
#                     'image': news.image,
#                     'slug': news.slug,
#                     'translation': {
#                         'language': translation.language,
#                         'title': translation.title,
#                         'content': translation.content,
#                         'short_description': translation.short_description
#                     }
#                 }
#                 return Response(data)
#             except NewsTranslation.DoesNotExist:
#                 return Response(
#                     {'error': 'Translation not found'}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )






















































# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from django.db.models import Q
# from .models import News, NewsTranslation
# from .serializers import NewsSerializer, NewsListSerializer, NewsTranslationSerializer
# from .pagination import NewsPagination

# class NewsListView(generics.ListAPIView):
#     serializer_class = NewsListSerializer
#     pagination_class = NewsPagination
    
#     def get_queryset(self):
#         queryset = News.objects.filter(is_published=True).order_by('-published_at')
        
#         page = self.kwargs.get('page', 1)
#         if page == 1 and not self.request.path.endswith('/1'):
#             page = 1
        
#         return queryset

# class NewsContentAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         identifier = kwargs.get('identifier')
#         language = request.GET.get('lang', 'en')
        
#         # Try to get by ID
#         if identifier.isdigit():
#             news = get_object_or_404(News, id=int(identifier), is_published=True)
#         # Try to get by slug
#         else:
#             translation = get_object_or_404(
#                 NewsTranslation, 
#                 slug=identifier
#             )
#             news = translation.news
#             if not news.is_published:
#                 return Response(
#                     {'error': 'News not found'}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )
        
#         # Get translation for requested language or fallback
#         try:
#             translation = news.translations.get(language=language)
#         except NewsTranslation.DoesNotExist:
#             try:
#                 translation = news.translations.get(language='en')
#             except NewsTranslation.DoesNotExist:
#                 return Response(
#                     {'error': 'Translation not found'}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )
        
#         serializer = NewsSerializer(news)
#         translation_serializer = NewsTranslationSerializer(translation)
        
#         response_data = serializer.data
#         response_data['translation'] = translation_serializer.data
        
#         return Response(response_data)

# class NewsCreateAPIView(generics.CreateAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class NewsUpdateAPIView(generics.UpdateAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_object(self):
#         obj = super().get_object()
#         # Optional: Add permission check here for author-only updates
#         # if obj.author != self.request.user:
#         #     raise permissions.PermissionDenied()
#         return obj






































# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from django.utils import timezone

# from .models import News, NewsTranslation
# from .serializers import NewsSerializer, NewsListSerializer, NewsTranslationSerializer
# from .pagination import NewsPagination


# class NewsViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet для работы с новостями.
#     """
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = NewsPagination
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['is_published']
#     search_fields = ['slug', 'translations__title', 'translations__content']
#     ordering_fields = ['published_at', 'created_at', 'updated_at']
#     ordering = ['-published_at']
#     lookup_field = 'slug'
    
#     def get_queryset(self):
#         """Возвращаем queryset в зависимости от действия"""
#         if self.action in ['list', 'retrieve']:
#             # Для публичных эндпоинтов показываем только опубликованные новости
#             return News.published.all()
#         return super().get_queryset()
    
#     def get_serializer_class(self):
#         """Используем разные сериализаторы для разных действий"""
#         if self.action == 'list':
#             return NewsListSerializer
#         return NewsSerializer
    
#     def list(self, request, *args, **kwargs):
#         """Переопределяем list для обработки различных параметров"""
#         # Проверяем наличие slug или id в query parameters
#         slug = request.query_params.get('slug')
#         news_id = request.query_params.get('id')
        
#         if slug:
#             # Возвращаем конкретную новость по slug
#             news = get_object_or_404(News.published, slug=slug)
#             serializer = self.get_serializer(news)
#             return Response(serializer.data)
        
#         if news_id:
#             # Возвращаем конкретную новость по id
#             news = get_object_or_404(News.published, id=news_id)
#             serializer = self.get_serializer(news)
#             return Response(serializer.data)
        
#         # Иначе возвращаем список с пагинацией
#         return super().list(request, *args, **kwargs)
    
#     @action(detail=False, methods=['get'], url_path='page/(?P<page_number>\d+)')
#     def page(self, request, page_number=None):
#         """Получение конкретной страницы новостей"""
#         try:
#             page_number = int(page_number)
#         except (TypeError, ValueError):
#             return Response(
#                 {'error': 'Номер страницы должен быть числом'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Получаем все опубликованные новости
#         queryset = News.published.all().order_by('-published_at')
        
#         # Создаем пагинатор
#         paginator = self.pagination_class()
        
#         # Получаем запрошенную страницу
#         page = paginator.paginate_queryset(queryset, request, page_number=page_number)
        
#         if page is None:
#             return Response(
#                 {'error': 'Страница не найдена'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         serializer = self.get_serializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
    
#     @action(detail=False, methods=['get'])
#     def latest(self, request):
#         """Получение последних 5 новостей"""
#         queryset = News.published.all().order_by('-published_at')[:5]
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def perform_create(self, serializer):
#         """Добавляем пользователя при создании новости"""
#         # Можно добавить логику для автоматической установки published_at
#         # если не указано явно
#         if 'published_at' not in serializer.validated_data:
#             serializer.validated_data['published_at'] = timezone.now()
        
#         serializer.save()
    
#     def destroy(self, request, *args, **kwargs):
#         """Переопределяем удаление для мягкого удаления или кастомной логики"""
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def perform_destroy(self, instance):
#         # Здесь можно реализовать мягкое удаление
#         # Например: instance.is_published = False
#         # instance.save()
#         instance.delete()


# class NewsTranslationViewSet(viewsets.ModelViewSet):
#     """ViewSet для управления переводами новостей"""
#     queryset = NewsTranslation.objects.all()
#     serializer_class = NewsTranslationSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """Фильтруем переводы по новости"""
#         news_id = self.kwargs.get('news_pk')
#         if news_id:
#             return NewsTranslation.objects.filter(news_id=news_id)
#         return super().get_queryset()
    
#     def perform_create(self, serializer):
#         """Привязываем перевод к новости"""
#         news_id = self.kwargs.get('news_pk')
#         news = get_object_or_404(News, id=news_id)
#         serializer.save(news=news)
































# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django.utils import timezone

# from .models import News, NewsTranslation
# from .serializers import (
#     NewsListSerializer, 
#     NewsDetailSerializer, 
#     NewsCreateSerializer
# )
# from .filters import NewsFilter




# LIMIT_NEWS = 5


# class NewsViewSet(viewsets.ModelViewSet):
#     queryset = News.objects.filter(is_published=True)
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_class = NewsFilter
#     search_fields = ['translations__title', 'translations__content']
#     ordering_fields = ['published_at', 'created_at']
#     ordering = ['-published_at']

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return NewsListSerializer
#         elif self.action == 'retrieve':
#             return NewsDetailSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return NewsCreateSerializer
#         return NewsDetailSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Фильтрация по дате публикации
#         if self.action == 'list':
#             queryset = queryset.filter(published_at__lte=timezone.now())
        
#         return queryset.prefetch_related('translations')

#     def list(self, request, *args, **kwargs):
#         """Список новостей с пагинацией"""
#         response = super().list(request, *args, **kwargs)
        
#         # Добавляем мета-информацию о языке
#         language = request.query_params.get('lang', 'en')
#         response.data['current_language'] = language
#         response.data['available_languages'] = dict(NewsTranslation.LANGUAGE_CHOICES)
        
#         return response

#     def retrieve(self, request, *args, **kwargs):
#         """Детальная информация о новости"""
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     @action(detail=True, methods=['get'])
#     def by_slug(self, request, slug=None):
#         """Получить новость по slug"""
#         try:
#             news = News.objects.get(slug=slug, is_published=True)
#             serializer = NewsDetailSerializer(
#                 news, 
#                 context={'request': request}
#             )
#             return Response(serializer.data)
#         except News.DoesNotExist:
#             return Response(
#                 {'error': 'News not found'}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )

#     @action(detail=False, methods=['get'])
#     def recent(self, request):
#         """Последние новости (ограниченное количество)"""
#         limit = int(request.query_params.get('limit', LIMIT_NEWS))
#         news = self.get_queryset()[:limit]
#         serializer = NewsListSerializer(
#             news, 
#             many=True, 
#             context={'request': request}
#         )
#         return Response(serializer.data)




# from rest_framework import viewsets
# from .models import News
# from .serializers import NewsSerializer

# class NewsViewSet(viewsets.ModelViewSet):
#     queryset = News.objects.all().order_by('-created_at')
#     serializer_class = NewsSerializer

