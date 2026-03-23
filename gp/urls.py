from django.contrib import admin
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=static('main/favicon.png'), permanent=True)),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('votes/', include('vote_system.urls')),
    path('forum/', include('forum.urls')),
    path('calendar/', include('event_calendar.urls')),
    path('user/', include('users.urls')),
    path('e_diary',include('e_diary.urls'))
]

