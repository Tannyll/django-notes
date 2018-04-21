from django.contrib import admin
from hello_palette.models import Palette


@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    pass
