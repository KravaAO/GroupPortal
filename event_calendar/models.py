from django.db import models


class CalendarEvent(models.Model):
	title = models.CharField(max_length=120)
	date = models.DateField()
	start_time = models.TimeField(blank=True, null=True)
	end_time = models.TimeField(blank=True, null=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["date", "start_time", "title"]
		verbose_name = "Calendar event"
		verbose_name_plural = "Calendar events"

	def __str__(self):
		return f"{self.title} ({self.date})"
