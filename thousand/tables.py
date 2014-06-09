import django_tables2 as tables
from django_tables2_reports.tables import TableReport
from timelines.models import ReporterList, MessagesList


class ReporterTable(TableReport):
    class Meta:
        model = ReporterList
        order_by = ('name')
        attrs = {
            'class': 'table table-striped table-bordered table-condensed'
        }


class StatsTable(TableReport):
    name = tables.Column(verbose_name="Item")
    value = tables.Column(verbose_name="Value")
    #details = tables.LinkColumn('reporters', verbose_name='Link for details')
    details = tables.URLColumn(attrs={"class": "myurl"})

    class Meta:
        attrs = {'class': 'table table-striped table-bordered table-condensed'}


class MessagesTable(TableReport):
    class Meta:
        model = MessagesList
        order_by = ('name')
        attrs = {
            'class': 'table table-striped table-bordered table-condensed'
        }
