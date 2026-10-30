# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
import uuid
import os


def avatar_upload_to(instance, filename):
    ext = filename.split('.')[-1].lower()
    return os.path.join("avatars", f"{uuid.uuid4().hex}.{ext}")



class User(AbstractUser):
    """
    Объект пользователя
    """
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    # avatar_img = models.ImageField(upload_to='avatars/', null=True, blank=True)
    avatar_img = models.ImageField(
        upload_to=avatar_upload_to,
        default="",
        blank=True,
        null=True
    )

    spirit_name = models.CharField(max_length=255, default="", null=True, blank=True)
    user_info = models.CharField(max_length=512, default="", null=True, blank=True)

    utc_offset = models.CharField(max_length=6, default='0')

    first = models.BooleanField(default=True)

    
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()  # кастомный менеджер

    def __str__(self):
        return self.email



class UserLink(models.Model):
    """
    Объект сылки
    """
    # link_type = models.ForeignKey(LinkType, on_delete=models.CASCADE, related_name='user_links')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='links'  # обратная связь: user.links.all()
    )
    name = models.CharField(max_length=20, default='link')
    url = models.CharField(max_length=255, blank=True, null=True)
    public = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.url:
            return self.url
        return ""
    
