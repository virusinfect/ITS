# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='get_layout_total')
def get_layout_total(group_totals, layout):
    return group_totals.get(layout, 0)
