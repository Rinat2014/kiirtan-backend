# moderators/model.py
from django.db import models
from users.models import User

class ModeratorSlot(models.Model):
    time = models.DateTimeField(unique=True)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moderators")
    is_regular = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time} - {self.moderator.username if self.moderator else 'Empty'}"
