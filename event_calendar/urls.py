from django.urls import path

from .views import add_event, day_events, delete_event, month_view

app_name = "event_calendar"

urlpatterns = [
    path("", month_view, name="month_view"),
    path("day-events/", day_events, name="day_events"),
    path("add-event/", add_event, name="add_event"),
    path("delete-event/<int:event_id>/", delete_event, name="delete_event"),
]
