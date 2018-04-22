from django.contrib import admin
from hello_palette.models import Palette


@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'colors', 'created_at', 'is_deleted')
    list_filter = ('is_deleted',)
    date_hierarchy = 'created_at'
