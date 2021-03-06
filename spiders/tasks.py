from __future__ import absolute_import, unicode_literals
from celery import task, chain, chord
from celery.utils.log import get_task_logger
import os
import sys
from .spiders_2 import Spiders, Parter, Concert, Karabas
from .import_db import ImportDb
from .get_facebook_events import Facebook

logger = get_task_logger(__name__)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'

import django
django.setup()
from events.models import Platform


@task(ignore_result=True, queue='mainchain')
def main_chain():
    try:
        return chain(
            chord([task_caribbean_parse.si()])(task_parsed_to_db.s()),
            chord([task_parter_parse.si()])(task_parsed_to_db.s()),
            chord([task_concert_parse.si()])(task_parsed_to_db.s()),
            chord([task_karabas_parse.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fc.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fs.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fj.si()])(task_parsed_to_db.s()),
            chord([task_facebook_parse_fh.si()])(task_parsed_to_db.s()),
        )().get()
    except TypeError:
        pass

@task(ignore_result=True, queue='todb')
def task_parsed_to_db(out_path):
    # Importing to Database
    import_ = ImportDb(out_path)
    added = import_.import_to_db()
    return added


# Main task

@task(ignore_result=True, queue='high')
def task_caribbean_parse():
    l_ = Spiders()
    path = l_.start_parse()
    return path


# Tickets tasks

@task(ignore_result=True, queue='normal')
def task_parter_parse():
    l_ = Parter()
    path = l_.not_async()
    return path


@task(ignore_result=True, queue='normal')
def task_concert_parse():
    l_ = Concert()
    path = l_.not_async()
    return path


@task(ignore_result=True, queue='normal')
def task_karabas_parse():
    l_ = Karabas()
    path = l_.async()
    return path


# Facebook tasks

queryset = Platform.objects.filter(
            name__startswith='fb_').values_list(
            'short_name', flat=True)
p_names = [x for x in queryset]


@task(ignore_result=False, queue='normal')
def task_facebook_parse_fc():
    fb = Facebook(p_names[0])
    return fb.process_dict()


@task(ignore_result=False, queue='normal')
def task_facebook_parse_fs():
    fb = Facebook(p_names[1])
    return fb.process_dict()


@task(ignore_result=False, queue='normal')
def task_facebook_parse_fj():
    fb = Facebook(p_names[2])
    return fb.process_dict()


@task(ignore_result=False, queue='normal')
def task_facebook_parse_fh():
    fb = Facebook(p_names[3])
    return fb.process_dict()
