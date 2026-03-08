from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Decide roles for users
class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    role_choices = [  
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default=USER)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
