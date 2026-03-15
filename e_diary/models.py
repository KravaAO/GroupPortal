from django.contrib.auth.models import User
from django.db import models


class Diary(models.Model):
    """
    Модель щоденника користувача.
    """

    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_profile.username


class Grade(models.Model):
    """
    Запис оцінки для конкретного щоденника.
    """

    user_profile = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name="grades")
    grade = models.SmallIntegerField()
    messege = models.TextField(default="")

    def __str__(self):
        return f"{self.user_profile}: {self.grade}"
