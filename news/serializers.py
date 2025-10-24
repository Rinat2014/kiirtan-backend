from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'













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
