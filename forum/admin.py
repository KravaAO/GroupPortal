from django.contrib import admin
from .models import Thread, Post


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("thread", "created_by", "created_at")
    search_fields = ("body",)
