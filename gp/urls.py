"""
URL configuration for gp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.templatetags.static import static as static_url
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
<<<<<<< HEAD
    path(
        "favicon.ico",
        RedirectView.as_view(url=static_url("main/favicon.png"), permanent=True),
    ),
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("portfolio/", include("portfolio.urls")),
    path("forum/", include("forum.urls")),
    path("calendar/", include("event_calendar.urls")),
    path("user/", include("users.urls")),
=======
    path('favicon.ico', RedirectView.as_view(url=static('main/favicon.png'), permanent=True)),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('votes/', include('vote_system.urls')),
    path('forum/', include('forum.urls')),
    path('calendar/', include('event_calendar.urls')),
    path('user/', include('users.urls')),
    path('e_diary/',include('e_diary.urls'))
>>>>>>> 19068e2248396c84f1c1809a090834156d241537
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
