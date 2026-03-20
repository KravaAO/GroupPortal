from django.urls import path
from . import views

urlpatterns = [
    path("settings/", views.settings_view, name="settings"),
    path("<str:username>/", views.portfolio_view, name="portfolio"),
    path("", views.my_portfolio_view, name="my_portfolio"),
    path("account-settings/", views.account_settings_view, name="account_settings"),
]
