from django.urls import path

from .views import home, section_page

urlpatterns = [
    path('', home, name='home'),
    path('sections/<slug:section_slug>/', section_page, name='section_page'),
]
