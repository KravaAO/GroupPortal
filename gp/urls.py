from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic.base import RedirectView

from e_diary.views import your_grades


urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=static("main/favicon.png"), permanent=True)),
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("forum/", include("forum.urls")),
    path("user/", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("newgrade/", your_grades.as_view()),
]
