# musicians/model.py
from django.db import models
from users.models import User

class MusicSlot(models.Model):
    time = models.DateTimeField(unique=True)
    musician = models.ForeignKey(User, on_delete=models.CASCADE, related_name="music_slots")
    is_regular = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time} - {self.musician.username if self.musician else 'Empty'}"
