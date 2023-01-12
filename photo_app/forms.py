from django import forms

from .models import Photo, Tag
from .models import TAGS, LOCATIONS


class PhotoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Photo
        fields = ('name', 'photo')


class DisplayForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name', 'photo')


class SearchForm(forms.Form):
    search = forms.CharField(label='search')


class TagForm(forms.Form):
    tags = forms.CharField(label='tags')

