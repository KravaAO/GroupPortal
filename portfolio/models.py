from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio_profile",
    )
    avatar = models.ImageField(upload_to="pictures/", blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/pictures/default-avatar.png"


class SocialLink(models.Model):
    SocialLink_CHOICES = [
        ("twitch", "Twitch"),
        ("youtube", "YouTube"),
        ("facebook", "Facebook"),
        ("twitter", "Twitter / X"),
        ("instagram", "Instagram"),
        ("discord", "Discord"),
        ("github", "GitHub"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="social_links",
    )
    platform = models.CharField(max_length=20, choices=SocialLink_CHOICES)
    url = models.URLField()

    class Meta:
        unique_together = ("user", "platform")

    def __str__(self):
        return f"{self.user.username} - {self.platform}"
