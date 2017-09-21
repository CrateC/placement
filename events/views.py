import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.views.generic import ListView
from utils.query_to_dict import convert_query_to_dict
from .tasks import get_query
from .models import Event
from .queries import SELECT_ID, DROP_TABLE
from .queries import MYSQL_CREATE_TEMP, MYSQL_LEFT_JOIN
from .queries import SQLITE3_CREATE_TEMP, SQLITE3_LEFT_JOIN


from django.core.cache import cache


class EventsPlacemenOrmView(LoginRequiredMixin, ListView):
    template_name = 'events/export.html'

    def get_queryset(self):
        # task_result = get_query.delay().get()
        #
        # # if you need to use the task_id somewhere else
        # # async_result = AsyncResult(id=task_result.id)
        # return task_result
        cache_key = 'Nlfjhdfyy!&pYEFmkFZN13451' # needs to be unique
        cache_time = 86400 # time in seconds for cache to be valid
        task_result = cache.get('task_result')
        if not task_result:
            task_result = get_query.delay().get()
            cache.set(cache_key, task_result, cache_time)
            # cache.set(
            #         'task_result',
            #         task_result,
            #         depends_on=[Event]
            # )
        return (task_result)



class EventsPlacementListView(LoginRequiredMixin, ListView):

    template_name = 'events/export.html'
    db_name = connection.settings_dict['NAME']
    tbl_names = ['CA', 'PA', 'CO', 'KA']

    @staticmethod
    def count_events(pl_id_):

        return Event.objects.filter(
                            platform='{}'.format(pl_id_),
                            date__gte=datetime.datetime.now(),
                            language='ru'
                ).order_by('date').count()

    # @staff_member_required
    def get_queryset(self):
        """
        SELECT_ID, DROP_TABLE
        """
        cursor = connection.cursor()
        columns = ['date', 'name']
        dc = {}

        for i, tbl_name in enumerate(self.tbl_names):

            cursor.execute(SELECT_ID.format(tbl_name))
            pl_id = cursor.fetchone()[0]

            if tbl_name in self.tbl_names:
                dc["{}".format(tbl_name)] = self.count_events(pl_id)

            cursor.execute(DROP_TABLE.format(tbl_name))
            #print(DROP_TABLE.format(tbl_name))

            if connection.vendor == 'mysql':
                """
                MYSQL_CREATE_TEMP, MYSQL_LEFT_JOIN
                """

                cursor.execute(f"{MYSQL_CREATE_TEMP.format(tbl_name)}")
                columns.append(tbl_name)

                if i == len(self.tbl_names)-1:

                    cursor.execute(MYSQL_LEFT_JOIN)
                    events_data = cursor.fetchall()
                    cursor.close()

            elif connection.vendor == 'sqlite3':
                """ SQLITE3_CREATE_TEMP, SQLITE3_LEFT_JOIN
                """

                cursor.execute(SQLITE3_CREATE_TEMP.format(tbl_name))
                columns.append(tbl_name)

                if tbl_name in max(self.tbl_names):
                    cursor.execute(SQLITE3_LEFT_JOIN)
                    events_data = cursor.fetchall()
                    cursor.close()

        return convert_query_to_dict(
                """{}""".format(events_data,))
