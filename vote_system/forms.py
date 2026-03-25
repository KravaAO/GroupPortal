from django import forms
from .models import Voting, Choice

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['title', 'description']
        widgets = {
            'title':
        forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Заголовок голосування'}),
            'description':
        forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder':'Опис...'}),
        }