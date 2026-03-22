from event_calendar.urls import urlpatterns
from event_calendar.urls import app_name
from django.urls import path
from e_diary.views import your_grades , teacher_crud 
app_name = "e_diary"

urlpatterns = [
    path("/your_diary",your_grades.as_view()),
    path("/teacher",teacher_crud.as_view),
        ]
