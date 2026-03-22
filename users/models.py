from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Profile for {self.user.username}"

    def is_moderator(self):
        return self.role == self.MODERATOR or self.user.is_staff

    def is_admin(self):
        return self.role == self.ADMIN or self.user.is_superuser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
