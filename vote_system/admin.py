from django.contrib import admin
from .models import Voting, Choice, Comment , Repost
# Register your models here.
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    inlines = [ChoiceInLine]

admin.site.register(Comment)
admin.site.register(Repost)