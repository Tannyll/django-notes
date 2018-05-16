from django import forms
from hello_palette.models import Palette


class PaletteForm(forms.ModelForm):
    class Meta:
        model = Palette
        exclude = ('is_deleted',)
