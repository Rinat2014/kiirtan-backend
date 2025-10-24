from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# add to group on register
gropu_musicians = "Musicians"

User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_musicians(sender, instance, created, **kwargs):
    if not created:
        return
    musicians, _ = Group.objects.get_or_create(name=gropu_musicians)
    instance.groups.add(musicians)
