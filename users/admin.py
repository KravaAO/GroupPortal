from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    # Дод. поле role у список в адмінці
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'bio', 'birth_date')}),
    )

admin.site.register(User, CustomUserAdmin)