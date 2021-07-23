from django import forms
from .models import Genre, Mark

ORDER_CHOICES = [
    ('mark', 'Rating ascending'),
    ('-mark', 'Rating descending'),
    ('release_year', 'Release year ascending'),
    ('-release_year', 'Release year descending'),
    ('title', 'Title (A-Z)'),
    ('-title', 'Title (Z-A)'),
]


class GenreForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.SelectMultiple(
        attrs={
            'class': 'form-select',
            'multiple': 'multiple',
        }
    ))
    order_by = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-select',
        }
    ), choices=ORDER_CHOICES)


class MovieMarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ("mark",)
        widgets = {
            "mark": forms.NumberInput(attrs={"max": 10, "default": 1})
        }
