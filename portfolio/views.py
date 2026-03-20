from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmailChangeForm, UsernameChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import Profile, SocialLink
from .forms import SocialLinkForm


@login_required
def my_portfolio_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    social_links = SocialLink.objects.filter(user=request.user)
    portfolio_user = {
        "username": request.user.username,
        "date_joined": request.user.date_joined,
        "profile": profile,
    }

    return render(
        request,
        "profile/portfolio.html",
        {"user": portfolio_user, "social_links": social_links},
    )


def portfolio_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user)
    social_links = SocialLink.objects.filter(user=user)
    portfolio_user = {
        "username": user.username,
        "date_joined": user.date_joined,
        "profile": profile,
    }

    return render(
        request,
        "profile/portfolio.html",
        {"user": portfolio_user, "social_links": social_links},
    )


@login_required
def settings_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if "reset_avatar" in request.POST:
            profile.avatar.delete(save=False)
            profile.avatar = None  # type: ignore
            profile.save()
            return redirect("settings")

        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
            profile.save()
            return redirect("settings")

        if "update_bio" in request.POST:
            profile.bio = request.POST.get("bio", "")
            profile.save()
            return redirect("settings")

    social_form = SocialLinkForm()
    social_links = SocialLink.objects.filter(user=request.user)
    portfolio_user = {
        "username": request.user.username,
        "email": request.user.email,
        "date_joined": request.user.date_joined,
        "profile": profile,
    }

    if request.method == "POST":
        if "add_social" in request.POST:
            social_form = SocialLinkForm(request.POST)
            if social_form.is_valid():
                link = social_form.save(commit=False)
                link.user = request.user
                link.save()
                return redirect("settings")

        elif "delete_social" in request.POST:
            link_id = request.POST.get("link_id")
            SocialLink.objects.filter(id=link_id, user=request.user).delete()
            return redirect("settings")

    return render(
        request,
        "profile/settings.html",
        {
            "user": portfolio_user,
            "profile": profile,
            "social_form": social_form,
            "social_links": social_links,
        },
    )


@login_required
def account_settings_view(request):
    username_form = UsernameChangeForm(instance=request.user)
    email_form = EmailChangeForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":

        if "change_username" in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                return redirect("account_settings")

        elif "change_email" in request.POST:
            email_form = EmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                return redirect("account_settings")

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect("account_settings")

        elif "delete_account" in request.POST:
            request.user.delete()
            return redirect("home")

    return render(
        request,
        "profile/account-settings.html",
        {
            "username_form": username_form,
            "email_form": email_form,
            "password_form": password_form,
        },
    )
