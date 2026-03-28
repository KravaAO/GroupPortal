from event_calendar.urls import urlpatterns
from event_calendar.urls import app_name
from django.urls import path
from e_diary.views import your_grades ,Note_create_view
app_name = "e_diary"

urlpatterns = [
    path("your_diary/",your_grades.as_view()),
    path("create_your_note/",Note_create_view.as_view())
    ]
