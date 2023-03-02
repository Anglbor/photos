from django import forms

from .models import Photo, Tag, Album
from .models import TAGS, LOCATIONS


class DateTimeSelector(forms.widgets.DateTimeInput):
    input_type = 'datetime-local'

class PhotoForm(forms.ModelForm):
    # this is not being in use due to js
    #tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Photo
        fields = ('name', 'photo', 'taken_date')
        widgets = {'taken_date': DateTimeSelector}


class DisplayForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name', 'photo')


class SearchForm(forms.Form):
    search = forms.CharField(label='search')


class TagForm(forms.Form):
    tags = forms.CharField(label='tags')


class AlbumForm(forms.Form):
    album_name = forms.CharField(label='album_name')