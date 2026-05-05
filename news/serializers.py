# backend/news/serializers.py
from rest_framework import serializers
from .models import News, NewsTranslation

class NewsTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTranslation
        fields = ['language', 'title', 'content', 'short_description']

class NewsListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'slug', 'title', 'short_description', 'author', 
                 'published_at', 'image', 'url']
    
    def get_translation(self, obj):
        """Получение перевода для текущего языка"""
        language = self.context.get('language', 'en')
        try:
            return obj.translations.get(language=language)
        except NewsTranslation.DoesNotExist:
            # Возвращаем английскую версию по умолчанию
            try:
                return obj.translations.get(language='en')
            except NewsTranslation.DoesNotExist:
                # Если нет английской версии, берем первую доступную
                return obj.translations.first()
    
    def get_title(self, obj):
        translation = self.get_translation(obj)
        return translation.title if translation else "No title"
    
    def get_short_description(self, obj):
        translation = self.get_translation(obj)
        return translation.short_description if translation else ""
    
    def get_url(self, obj):
        """Генерируем URL для новости"""
        request = self.context.get('request')
        if request:
            # Формируем URL вручную
            base_url = request.build_absolute_uri('/')
            # Можно выбрать один из вариантов:
            # 1. По ID: /api/news/content/1/
            # 2. По slug: /api/news/content/slug/
            return f"{base_url}api/news/content/{obj.slug}/"
        return f"/api/news/content/{obj.slug}/"

class NewsDetailSerializer(NewsListSerializer):
    content = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = ['id', 'slug', 'title', 'content', 'short_description', 
                 'author', 'published_at', 'image', 'url']
    
    def get_content(self, obj):
        translation = self.get_translation(obj)
        return translation.content if translation else ""





































# from rest_framework import serializers
# from .models import News, NewsTranslation

# class NewsTranslationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewsTranslation
#         fields = ['language', 'title', 'content', 'short_description']
#         read_only_fields = ['news']

# class NewsSerializer(serializers.ModelSerializer):
#     translations = NewsTranslationSerializer(many=True, required=False)
#     current_translation = serializers.SerializerMethodField()
    
#     class Meta:
#         model = News
#         fields = ['id', 'author', 'published_at', 'is_published', 
#                  'image', 'slug', 'translations', 'current_translation']
#         read_only_fields = ['slug']
    
#     def get_current_translation(self, obj):
#         """
#         Возвращает перевод на основе языка из запроса
#         """
#         request = self.context.get('request')
#         if request:
#             # Получаем язык из query параметров или заголовков
#             lang = request.query_params.get('lang', 'en')
            
#             # Ищем перевод для данного языка
#             try:
#                 translation = obj.translations.get(language=lang)
#                 return NewsTranslationSerializer(translation).data
#             except NewsTranslation.DoesNotExist:
#                 # Если перевод не найден, пытаемся получить английскую версию
#                 try:
#                     translation = obj.translations.get(language='en')
#                     return NewsTranslationSerializer(translation).data
#                 except NewsTranslation.DoesNotExist:
#                     # Если английской тоже нет, возвращаем первый доступный
#                     first_translation = obj.translations.first()
#                     if first_translation:
#                         return NewsTranslationSerializer(first_translation).data
#         return None
    
#     def create(self, validated_data):
#         translations_data = validated_data.pop('translations', [])
#         news = News.objects.create(**validated_data)
        
#         for translation_data in translations_data:
#             NewsTranslation.objects.create(news=news, **translation_data)
        
#         return news
    
#     def update(self, instance, validated_data):
#         translations_data = validated_data.pop('translations', None)
        
#         # Обновляем основную модель
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
        
#         # Обновляем переводы, если они есть в данных
#         if translations_data is not None:
#             # Удаляем старые переводы и создаем новые
#             instance.translations.all().delete()
#             for translation_data in translations_data:
#                 NewsTranslation.objects.create(news=instance, **translation_data)
        
#         return instance









































# from rest_framework import serializers
# from .models import News, NewsTranslation

# class NewsTranslationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewsTranslation
#         fields = ['id', 'language', 'title', 'slug', 'content', 'short_description']
#         read_only_fields = ['id', 'slug']

# class NewsSerializer(serializers.ModelSerializer):
#     translations = NewsTranslationSerializer(many=True, required=False)
    
#     class Meta:
#         model = News
#         fields = ['id', 'author', 'published_at', 'is_published', 'image', 'translations']
#         read_only_fields = ['id', 'author', 'published_at']
    
#     def create(self, validated_data):
#         translations_data = validated_data.pop('translations', [])
#         request = self.context.get('request')
        
#         if request and hasattr(request, 'user'):
#             validated_data['author'] = request.user
        
#         news = News.objects.create(**validated_data)
        
#         for translation_data in translations_data:
#             NewsTranslation.objects.create(news=news, **translation_data)
        
#         return news
    
#     def update(self, instance, validated_data):
#         translations_data = validated_data.pop('translations', [])
        
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
        
#         for translation_data in translations_data:
#             language = translation_data.get('language')
#             translation, created = NewsTranslation.objects.update_or_create(
#                 news=instance,
#                 language=language,
#                 defaults=translation_data
#             )
        
#         return instance

# class NewsListSerializer(serializers.ModelSerializer):
#     translation = serializers.SerializerMethodField()
    
#     class Meta:
#         model = News
#         fields = ['id', 'author', 'published_at', 'image', 'translation']
    
#     def get_translation(self, obj):
#         request = self.context.get('request')
#         language = request.GET.get('lang', 'en') if request else 'en'
        
#         try:
#             translation = obj.translations.get(language=language)
#             return {
#                 'title': translation.title,
#                 'slug': translation.slug,
#                 'short_description': translation.short_description
#             }
#         except NewsTranslation.DoesNotExist:
#             # Fallback to English if requested language not found
#             try:
#                 translation = obj.translations.get(language='en')
#                 return {
#                     'title': translation.title,
#                     'slug': translation.slug,
#                     'short_description': translation.short_description
#                 }
#             except NewsTranslation.DoesNotExist:
#                 return None































# from rest_framework import serializers
# from .models import News, NewsTranslation, LANGUAGE_CHOICES
# from django.utils import timezone




# class NewsTranslationSerializer(serializers.ModelSerializer):
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    
#     class Meta:
#         model = NewsTranslation
#         fields = ['language', 'title', 'content', 'excerpt']
#         read_only_fields = ['created_at', 'updated_at']


# class NewsSerializer(serializers.ModelSerializer):
#     translations = NewsTranslationSerializer(many=True, required=False)
#     translation = serializers.SerializerMethodField()
    
#     class Meta:
#         model = News
#         fields = [
#             'id', 'slug', 'image', 'published_at', 
#             'is_published', 'created_at', 'updated_at',
#             'translations', 'translation'
#         ]
#         read_only_fields = ['created_at', 'updated_at']
#         extra_kwargs = {
#             'slug': {'required': False},
#             'image': {'required': False},
#         }
    
#     def get_translation(self, obj):
#         """Получить перевод для текущего языка запроса"""
#         request = self.context.get('request')
#         if request:
#             # Определяем язык из заголовка Accept-Language или параметра
#             language = request.GET.get('lang') or request.META.get('HTTP_ACCEPT_LANGUAGE', 'en').split(',')[0][:2]
            
#             # Проверяем, что язык есть в наших choices
#             valid_languages = [code for code, _ in LANGUAGE_CHOICES]
#             if language not in valid_languages:
#                 language = 'en'  # язык по умолчанию
            
#             translation = obj.get_translation(language)
#             if translation:
#                 return NewsTranslationSerializer(translation).data
#         return None
    
#     def create(self, validated_data):
#         translations_data = validated_data.pop('translations', [])
        
#         # Генерируем slug если не предоставлен
#         if 'slug' not in validated_data or not validated_data['slug']:
#             # Можно использовать UUID или другой метод генерации
#             import uuid
#             validated_data['slug'] = str(uuid.uuid4())[:8]
        
#         news = News.objects.create(**validated_data)
        
#         # Создаем переводы
#         for translation_data in translations_data:
#             NewsTranslation.objects.create(news=news, **translation_data)
        
#         return news
    
#     def update(self, instance, validated_data):
#         translations_data = validated_data.pop('translations', [])
        
#         # Обновляем основные поля новости
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
        
#         # Обновляем или создаем переводы
#         if translations_data:
#             existing_translations = {t.language: t for t in instance.translations.all()}
            
#             for translation_data in translations_data:
#                 language = translation_data['language']
#                 if language in existing_translations:
#                     # Обновляем существующий перевод
#                     translation = existing_translations[language]
#                     for attr, value in translation_data.items():
#                         setattr(translation, attr, value)
#                     translation.save()
#                 else:
#                     # Создаем новый перевод
#                     NewsTranslation.objects.create(news=instance, **translation_data)
        
#         return instance


# class NewsListSerializer(NewsSerializer):
#     """Упрощенный сериализатор для списка новостей"""
#     class Meta:
#         model = News
#         fields = ['id', 'slug', 'image', 'published_at', 'translation']
    
#     def to_representation(self, instance):
#         """Переопределяем для компактного представления"""
#         representation = super().to_representation(instance)
        
#         # Оставляем только необходимые поля из перевода
#         if representation.get('translation'):
#             translation = representation['translation']
#             representation['title'] = translation.get('title')
#             representation['excerpt'] = translation.get('excerpt')
#             del representation['translation']
        
#         return representation




































# # news/serializers.py
# from rest_framework import serializers
# from .models import News, NewsTranslation




# class NewsTranslationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewsTranslation
#         fields = [
#             'language', 
#             'title', 
#             'content', 
#             'excerpt',
#             'meta_title', 
#             'meta_description'
#         ]

# class NewsCreateSerializer(serializers.ModelSerializer):
#     translations = NewsTranslationSerializer(many=True)

#     class Meta:
#         model = News
#         fields = [
#             'slug', 
#             'image', 
#             'published_at', 
#             'is_published', 
#             'translations'
#         ]

#     def create(self, validated_data):
#         translations_data = validated_data.pop('translations')
#         news = News.objects.create(**validated_data)
        
#         for translation_data in translations_data:
#             NewsTranslation.objects.create(news=news, **translation_data)
        
#         return news

#     def update(self, instance, validated_data):
#         translations_data = validated_data.pop('translations', None)
        
#         # Обновляем основные поля новости
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
        
#         # Обновляем переводы
#         if translations_data is not None:
#             # Удаляем старые переводы и создаем новые
#             instance.translations.all().delete()
#             for translation_data in translations_data:
#                 NewsTranslation.objects.create(news=instance, **translation_data)
        
#         return instance

# class NewsListSerializer(serializers.ModelSerializer):
#     title = serializers.SerializerMethodField()
#     excerpt = serializers.SerializerMethodField()
#     content_preview = serializers.SerializerMethodField()

#     class Meta:
#         model = News
#         fields = [
#             'id',
#             'slug', 
#             'title',
#             'excerpt',
#             'content_preview',
#             'image', 
#             'published_at',
#             'created_at'
#         ]

#     def get_title(self, obj):
#         request = self.context.get('request')
#         language = request.query_params.get('lang', 'en') if request else 'en'
#         translation = obj.get_translation(language)
#         return translation.title if translation else None

#     def get_excerpt(self, obj):
#         request = self.context.get('request')
#         language = request.query_params.get('lang', 'en') if request else 'en'
#         translation = obj.get_translation(language)
#         return translation.excerpt if translation else None

#     def get_content_preview(self, obj):
#         request = self.context.get('request')
#         language = request.query_params.get('lang', 'en') if request else 'en'
#         translation = obj.get_translation(language)
#         if translation and translation.content:
#             return translation.content[:150] + '...' if len(translation.content) > 150 else translation.content
#         return None

# class NewsDetailSerializer(serializers.ModelSerializer):
#     translation = serializers.SerializerMethodField()
#     available_languages = serializers.SerializerMethodField()

#     class Meta:
#         model = News
#         fields = [
#             'id',
#             'slug',
#             'image',
#             'published_at',
#             'created_at',
#             'updated_at',
#             'translation',
#             'available_languages'
#         ]

#     def get_translation(self, obj):
#         request = self.context.get('request')
#         language = request.query_params.get('lang', 'en') if request else 'en'
#         translation = obj.get_translation(language)
        
#         if translation:
#             return NewsTranslationSerializer(translation).data
#         return None

#     def get_available_languages(self, obj):
#         return list(obj.translations.values_list('language', flat=True))


# from rest_framework import serializers
# from .models import News

# class NewsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = News
#         fields = '__all__'













# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import News

# User = get_user_model()


# class AuthorSimpleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("id", "username", "email")


# # Сериализатор для отдачи новости (читает перевод по lang из request или fallback)
# class NewsSerializer(serializers.ModelSerializer):
#     title = serializers.SerializerMethodField()
#     text_annotation = serializers.SerializerMethodField()
#     text_content = serializers.SerializerMethodField()
#     date = serializers.DateTimeField(source="created_at", read_only=True)
#     date_edit = serializers.DateTimeField(source="updated_at", read_only=True)
#     author = AuthorSimpleSerializer(read_only=True)

#     class Meta:
#         model = News
#         fields = (
#             "id",
#             "title",
#             "date",
#             "date_edit",
#             "author",
#             "text_annotation",
#             "text_content",
#             "img_link",
#             "img_alt",
#         )

#     def _get_translation_field(self, obj, field_name):
#         request = self.context.get("request", None)
#         lang = None
#         if request is not None:
#             lang = request.GET.get("lang") or getattr(request, "LANGUAGE_CODE", None)
#         if not lang:
#             lang = "en"  # fallback default

#         # Parler хранит переводы в related manager `translations` с полем language_code
#         tr = obj.translations.filter(language_code=lang).first()
#         if tr and getattr(tr, field_name):
#             return getattr(tr, field_name)
#         # fallback - любое доступное
#         tr = obj.translations.first()
#         return getattr(tr, field_name) if tr else None

#     def get_title(self, obj):
#         return self._get_translation_field(obj, "title")

#     def get_text_annotation(self, obj):
#         return self._get_translation_field(obj, "text_annotation")

#     def get_text_content(self, obj):
#         return self._get_translation_field(obj, "text_content")


# # Сериализатор для создания/обновления — принимает поле `translations`
# class NewsCreateUpdateSerializer(serializers.ModelSerializer):
#     # ожидаем: { "ru": {"title":..., "text_annotation":..., "text_content":...}, "en": { ... } }
#     translations = serializers.DictField(child=serializers.DictField(), write_only=True)

#     class Meta:
#         model = News
#         fields = ("id", "translations", "img_link", "img_alt")

#     def validate_translations(self, value):
#         """
#         Проверяем, что есть оба языка (или как минимум обязательный набор).
#         Можно сделать более гибко — сейчас требуем ru и en.
#         """
#         required_langs = {"ru", "en"}
#         missing = required_langs - set(value.keys())
#         if missing:
#             raise serializers.ValidationError(f"Missing translations for: {', '.join(missing)}")
#         # проверим обязательные поля внутри
#         for lang, data in value.items():
#             if "title" not in data:
#                 raise serializers.ValidationError(f"'{lang}' translation must contain 'title'")
#         return value

#     def create(self, validated_data):
#         translations = validated_data.pop("translations")
#         request = self.context.get("request")
#         author = getattr(request, "user", None) if request and request.user.is_authenticated else None

#         news = News.objects.create(author=author, **validated_data)

#         # создаём переводы по языкам
#         for lang, fields in translations.items():
#             news.set_current_language(lang)
#             for k, v in fields.items():
#                 setattr(news, k, v)
#             news.save()  # сохраняем перевод

#         return news

#     def update(self, instance, validated_data):
#         translations = validated_data.pop("translations", None)
#         # обновляем non-translated поля
#         for attr, val in validated_data.items():
#             setattr(instance, attr, val)
#         instance.save()

#         if translations:
#             # обновляем те переводы, которые пришли
#             for lang, fields in translations.items():
#                 instance.set_current_language(lang)
#                 for k, v in fields.items():
#                     setattr(instance, k, v)
#                 instance.save()
#         return instance
