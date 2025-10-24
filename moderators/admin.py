# moderators/admin.py
from django.contrib import admin
from .models import ModeratorSlot

@admin.register(ModeratorSlot)
class ModeratorSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_regular', 'time', 'moderator')
    # list_filter = ('is_active', 'is_musician', 'is_moderator_musicians', 'is_editor', 'is_admin', 'is_moderator_site')