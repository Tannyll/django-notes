from django import template

register = template.Library()


@register.inclusion_tag('includes/color_boxes.html')
def include_color_boxes(palette):
    context_data = {
        'colors': palette.colors_as_list
    }
    return context_data
