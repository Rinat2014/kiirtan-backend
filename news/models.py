# news/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class News(models.Model):
    author = models.CharField(max_length=200)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    image = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = _('News')
        verbose_name_plural = _('News')
    
    def __str__(self):
        return f"News {self.id} by {self.author}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем slug на основе ID
            if self.id:
                self.slug = f"news-{self.id}"
            else:
                # Если объект еще не сохранен, временный slug
                super().save(*args, **kwargs)
                self.slug = f"news-{self.id}"
                kwargs['force_insert'] = False
        super().save(*args, **kwargs)

class NewsTranslation(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Russian'),
    ]
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    title = models.CharField(max_length=200)
    content = models.TextField()
    short_description = models.TextField(max_length=500)
    
    class Meta:
        unique_together = [['news', 'language']]
        verbose_name = _('News Translation')
        verbose_name_plural = _('News Translations')
    
    def __str__(self):
        return f"{self.title} ({self.language})"































# from django.db import models
# from django.conf import settings
# from django.utils.text import slugify
# from django.utils.translation import gettext_lazy as _

# class News(models.Model):
#     author = models.CharField(max_length=100)
#     published_at = models.DateTimeField(auto_now_add=True)
#     is_published = models.BooleanField(default=True)
#     image = models.URLField(blank=True, null=True)
#     slug = models.SlugField(max_length=200, unique=True)
    
#     def __str__(self):
#         return f"News {self.id} by {self.author}"
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             # Генерируем slug из id, если нужно, или добавьте поле для генерации
#             self.slug = f"news-{self.id}"
#         super().save(*args, **kwargs)

# class NewsTranslation(models.Model):
#     LANGUAGE_CHOICES = [
#         ('en', 'English'),
#         ('ru', 'Russian'),
#     ]
    
#     news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='translations')
#     language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     short_description = models.TextField(max_length=500)
    
#     class Meta:
#         unique_together = [['news', 'language']]
#         indexes = [
#             models.Index(fields=['news', 'language']),
#         ]
    
#     def __str__(self):
#         return f"{self.title} ({self.language})"

































# from django.db import models
# from django.conf import settings
# from django.utils.text import slugify
# from django.utils.translation import gettext_lazy as _

# class News(models.Model):
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='news_posts'
#     )
#     published_at = models.DateTimeField(auto_now_add=True)
#     is_published = models.BooleanField(default=True)
#     image = models.URLField(blank=True, null=True)
    
#     def __str__(self):
#         return f"News {self.id} by {self.author.username}"

# class NewsTranslation(models.Model):
#     LANGUAGE_CHOICES = [
#         ('en', 'English'),
#         ('ru', 'Russian'),
#     ]
    
#     news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='translations')
#     language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=False)
#     content = models.TextField()
#     short_description = models.TextField(max_length=500)
    
#     class Meta:
#         unique_together = [['news', 'language']]
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f"{self.title} ({self.language})"
