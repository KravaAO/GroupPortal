from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class UserUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "bio",
            "birth_date",
            "profile_picture",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = getattr(self.instance, "profile", None)
        if profile:
            self.fields["bio"].initial = profile.bio
            self.fields["birth_date"].initial = profile.birth_date
            self.fields["profile_picture"].initial = profile.profile_picture

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.bio = self.cleaned_data.get("bio")
        profile.birth_date = self.cleaned_data.get("birth_date")

        profile_picture = self.cleaned_data.get("profile_picture")
        if profile_picture is not None:
            profile.profile_picture = profile_picture

        profile.save()
        return user


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # Додаємо клас 'input', щоб твій CSS спрацював
            field.widget.attrs.update({"class": "input"})
