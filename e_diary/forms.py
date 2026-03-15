from django import forms

from e_diary.models import Grade


class add_grade(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["grade", "messege"]

