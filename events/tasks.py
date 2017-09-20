from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger

from .get_view_data import get_queryset_data
from utils.query_to_dict import convert_qslist_to_dict

logger = get_task_logger(__name__)

@shared_task(queue='page_load')
def get_query():
    return convert_qslist_to_dict("""{}""".format(get_queryset_data(),))
