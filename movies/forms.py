from django import forms
from .models import Genre


class GenreForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.SelectMultiple(
        attrs={
            'class': 'form-select',
            'multiple': 'multiple',
        }
    ))
