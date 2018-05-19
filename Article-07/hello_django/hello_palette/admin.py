from django.contrib import admin
from django.utils.html import format_html
from hello_palette.models import Palette


@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_colors', 'created_at', 'is_deleted')
    list_filter = ('is_deleted',)
    date_hierarchy = 'created_at'

    def get_colors(self, obj):
        circle_template = '<svg width=16 height=16><circle cx=8 cy=8 r=5 style="fill: {};"></circle></svg>'
        return format_html(''.join(circle_template.format(c) for c in obj.colors_as_list))

    get_colors.short_description = "Colors"
    get_colors.allow_tags = True
