from django.urls import path
from . import views

urlpatterns = [
    path("portfolio/<str:username>/", views.portfolio_view, name="portfolio"),
    path("portfolio/", views.my_portfolio_view, name="my_portfolio"),
    path("settings/", views.settings_view, name="settings"),
    path("account-settings/", views.account_settings_view, name="account_settings"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
