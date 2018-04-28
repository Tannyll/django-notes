from django import template

register = template.Library()


@register.inclusion_tag('includes/color_boxes.html')
def include_color_boxes(colors):
    context_data = {
        'colors': colors.split(',')
    }
    return context_data
