from django.contrib import admin

from .models import CalendarEvent


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
	list_display = ("title", "date", "start_time", "end_time")
	list_filter = ("date",)
	search_fields = ("title", "description")
