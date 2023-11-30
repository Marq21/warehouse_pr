from django import template
import catalog.views as views


register = template.Library()

@register.simple_tag()
def get_categories():
    return views.show_category