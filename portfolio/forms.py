from typing import Any
from django import forms
from django.contrib.auth.models import User
from .models import SocialLink


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Новий username"}
            )
        }


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Новий email"}
            )
        }


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["platform", "url"]
        widgets = {
            "platform": forms.Select(attrs={"class": "form-select"}),
            "url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://..."}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        platform = cleaned_data.get("platform")
        url = cleaned_data.get("url")

        if platform and url:
            expected_domains = {
                "twitch": "twitch.tv",
                "youtube": "youtube.com",
                "facebook": "facebook.com",
                "twitter": "twitter.com",
                "instagram": "instagram.com",
                "discord": "discord.gg",
                "github": "github.com",
            }
            expected_domain = expected_domains.get(platform)

            if expected_domain not in url:
                raise forms.ValidationError(
                    f"Для {platform} дозволені лише посилання з доменом {expected_domain}"
                )
        return cleaned_data
