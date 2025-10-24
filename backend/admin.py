from django.contrib import admin
from django.contrib.auth.models import Group

# Сначала снимем регистрацию стандартного Group
admin.site.unregister(Group)

# Регистрируем заново с кастомным админом
@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # здесь указываем поля для отображения
    ordering = ("id",)              # сортировка по id (опционально)
