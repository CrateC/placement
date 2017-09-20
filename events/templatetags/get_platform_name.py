import os
import sys
import django

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))))
print(PROJECT_DIR)
sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'
django.setup()

from events.models import Platform

from django import template

register = template.Library()

@register.simple_tag
def platform_name(key):
    name = Platform.objects.filter(short_name=key).values_list('name', flat=True)[0]
    return name
