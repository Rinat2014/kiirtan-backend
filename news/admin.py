# backend/news/admin.py
from django.contrib import admin
from .models import News, NewsTranslation

class NewsTranslationInline(admin.TabularInline):
    model = NewsTranslation
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'published_at', 'is_published', 'slug']
    list_filter = ['is_published', 'published_at']
    search_fields = ['author', 'slug', 'translations__title']
    inlines = [NewsTranslationInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.slug and obj.id:
            obj.slug = f"news-{obj.id}"
        super().save_model(request, obj, form, change)

@admin.register(NewsTranslation)
class NewsTranslationAdmin(admin.ModelAdmin):
    list_display = ['title', 'news', 'language', 'short_description']
    list_filter = ['language']
    search_fields = ['title', 'content']



























# from django.contrib import admin
# from .models import News, NewsTranslation

# class NewsTranslationInline(admin.TabularInline):
#     model = NewsTranslation
#     extra = 1

# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ['id', 'author', 'published_at', 'is_published', 'slug']
#     list_filter = ['is_published', 'published_at']
#     search_fields = ['author', 'translations__title']
#     inlines = [NewsTranslationInline]
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('translations')

# @admin.register(NewsTranslation)
# class NewsTranslationAdmin(admin.ModelAdmin):
#     list_display = ['title', 'news', 'language', 'short_description']
#     list_filter = ['language']
#     search_fields = ['title', 'content']








































# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
# from .models import News, NewsTranslation

# class NewsTranslationInline(admin.TabularInline):
#     model = NewsTranslation
#     extra = 1
#     max_num = 2  # Ограничиваем количеством языков (EN и RU)
#     fields = ('language', 'title', 'slug', 'short_description', 'content')
#     readonly_fields = ('slug',)

# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'get_title', 'author', 'published_at', 'is_published', 'image_preview')
#     list_display_links = ('id', 'get_title')
#     list_filter = ('is_published', 'published_at', 'author')
#     search_fields = ('translations__title', 'translations__content', 'author__username')
#     date_hierarchy = 'published_at'
#     list_per_page = 20
#     fieldsets = (
#         (_('Основная информация'), {
#             'fields': ('author', 'is_published', 'image')
#         }),
#         (_('Даты'), {
#             'fields': ('published_at',),
#             'classes': ('collapse',)
#         }),
#     )
#     readonly_fields = ('published_at',)
#     inlines = [NewsTranslationInline]
    
#     def get_title(self, obj):
#         # Получаем английскую версию заголовка для отображения в списке
#         try:
#             en_translation = obj.translations.get(language='en')
#             return en_translation.title
#         except NewsTranslation.DoesNotExist:
#             try:
#                 # Если английской версии нет, берем первую доступную
#                 translation = obj.translations.first()
#                 return f"{translation.title} ({translation.language})"
#             except:
#                 return _("Нет перевода")
#     get_title.short_description = _('Заголовок')
#     get_title.admin_order_field = 'translations__title'
    
#     def image_preview(self, obj):
#         if obj.image:
#             return f'<a href="{obj.image}" target="_blank"><img src="{obj.image}" style="max-height: 50px; max-width: 50px;" /></a>'
#         return _("Нет изображения")
#     image_preview.short_description = _('Изображение')
#     image_preview.allow_tags = True

# class NewsTranslationAdmin(admin.ModelAdmin):
#     list_display = ('title', 'language', 'news_id', 'news_author', 'short_description_preview')
#     list_filter = ('language', 'news__author')
#     search_fields = ('title', 'content', 'news__author__username')
#     list_per_page = 20
#     fieldsets = (
#         (_('Основная информация'), {
#             'fields': ('news', 'language', 'title', 'slug')
#         }),
#         (_('Содержание'), {
#             'fields': ('short_description', 'content')
#         }),
#     )
#     readonly_fields = ('slug',)
    
#     def news_id(self, obj):
#         return obj.news.id
#     news_id.short_description = _('ID новости')
    
#     def news_author(self, obj):
#         return obj.news.author.username
#     news_author.short_description = _('Автор')
    
#     def short_description_preview(self, obj):
#         if len(obj.short_description) > 100:
#             return f"{obj.short_description[:100]}..."
#         return obj.short_description
#     short_description_preview.short_description = _('Краткое описание')

# # Регистрация моделей в админке
# admin.site.register(News, NewsAdmin)
# admin.site.register(NewsTranslation, NewsTranslationAdmin)

# # Опционально: улучшаем заголовок админки
# admin.site.site_header = _('Панель управления новостями')
# admin.site.site_title = _('Админка новостей')
# admin.site.index_title = _('Управление новостями')


