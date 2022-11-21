from django import template
from app_main.models import StatusFlow

register = template.Library()


@register.filter()
def to_int(value):
    return int(value)


@register.simple_tag(name='line_color')
def get_color(status):
    return status.color


@register.simple_tag(name='line_element')
def get_elements(status):
    return StatusFlow.objects.filter(current_status_id=status.id)
