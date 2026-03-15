from django import forms
from .models import Thread, Post


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Thread title cannot be empty.")
        return title


class PostForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}),
        required=False,
    )

    class Meta:
        model = Post
        fields = ["body"]

    def clean_body(self):
        body = self.cleaned_data.get("body", "").strip()
        if not body:
            raise forms.ValidationError("Message cannot be empty.")
        return body
