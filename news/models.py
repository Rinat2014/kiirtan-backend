from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news_images/')
    short_text = models.TextField()
    full_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title












# from django.db import models
# from django.conf import settings
# from parler.models import TranslatableModel, TranslatedFields


# class News(TranslatableModel):
#     translations = TranslatedFields(
#         title=models.CharField(max_length=255),
#         text_annotation=models.TextField(blank=True),
#         text_content=models.TextField(blank=True),
#     )

#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name="news", on_delete=models.SET_NULL, null=True
#     )
#     img_link = models.URLField(blank=True, null=True)
#     img_alt = models.CharField(max_length=255, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ("-created_at",)

#     def __str__(self):
#         return self.safe_translation_getter("title", any_language=True) or f"News {self.pk}"

