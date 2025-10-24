from django.contrib import admin
from .models import MusicSlot

@admin.register(MusicSlot)
class MusicSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_regular', 'time', 'musician')
