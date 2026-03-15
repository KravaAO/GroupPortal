from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from e_diary.models import Diary


@receiver(post_save, sender=get_user_model())
def create_diary_for_new_user(sender, instance, created, **kwargs):
    if created:
        Diary.objects.get_or_create(user_profile=instance)
