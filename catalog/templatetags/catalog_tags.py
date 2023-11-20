from django import template
import catalog.views as views
from catalog.models import Category


register = template.Library()

@register.simple_tag()
def get_categories():
    return views.show_category