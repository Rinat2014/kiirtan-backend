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
    

# bereal
# clubhouse
# discord
# douyin
# facebook
# instagram
# kakaotalk
# kuaishou
# line
# linkedin
# ok
# pinterest
# qq
# reddit
# snapchat
#     telegram
# threads
# tiktok
# tumblr
# vkontakte
# wechat
# weibo
# whatsapp
# x
# youtube


    # links = models.ManyToManyField(UserLink, related_name='users', blank=True)
    # links = models.ForeignKey(UserLink, on_delete=models.CASCADE, related_name='links', null=True, blank=True)

    
    # Социальные сети в алфавитном порядке
    # social_bereal       = models.URLField(max_length=255, null=True, blank=True)
    # social_clubhouse    = models.URLField(max_length=255, null=True, blank=True)
    # social_discord      = models.URLField(max_length=255, null=True, blank=True)
    # social_douyin       = models.URLField(max_length=255, null=True, blank=True)
    # social_facebook     = models.URLField(max_length=255, null=True, blank=True)
    # social_instagram    = models.URLField(max_length=255, null=True, blank=True)
    # social_kakaotalk    = models.URLField(max_length=255, null=True, blank=True)
    # social_kuaishou     = models.URLField(max_length=255, null=True, blank=True)
    # social_line         = models.URLField(max_length=255, null=True, blank=True)
    # social_linkedin     = models.URLField(max_length=255, null=True, blank=True)
    # social_ok           = models.URLField(max_length=255, null=True, blank=True)
    # social_pinterest    = models.URLField(max_length=255, null=True, blank=True)
    # social_qq           = models.URLField(max_length=255, null=True, blank=True)
    # social_reddit       = models.URLField(max_length=255, null=True, blank=True)
    # social_snapchat     = models.URLField(max_length=255, null=True, blank=True)
    # social_telegram     = models.URLField(max_length=255, null=True, blank=True)
    # social_threads      = models.URLField(max_length=255, null=True, blank=True)
    # social_tiktok       = models.URLField(max_length=255, null=True, blank=True)
    # social_tumblr       = models.URLField(max_length=255, null=True, blank=True)
    # social_vkontakte    = models.URLField(max_length=255, null=True, blank=True)
    # social_wechat       = models.URLField(max_length=255, null=True, blank=True)
    # social_weibo        = models.URLField(max_length=255, null=True, blank=True)
    # social_whatsapp     = models.URLField(max_length=255, null=True, blank=True)
    # social_x            = models.URLField(max_length=255, null=True, blank=True)
    # social_youtube      = models.URLField(max_length=255, null=True, blank=True)

    # is_musician             = models.BooleanField(default=True)
    # is_moderator_musicians  = models.BooleanField(default=False)
    # is_editor               = models.BooleanField(default=False)
    # is_moderator_site       = models.BooleanField(default=False)
    # is_admin                = models.BooleanField(default=False)
    # is_active               = models.BooleanField(default=False)  # Неактивный, пока не подтвердит email