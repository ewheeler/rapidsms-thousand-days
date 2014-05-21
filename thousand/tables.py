import django_tables2 as tables
from timelines.models import ReporterList


class ReporterTable(tables.Table):
    class Meta:
        model = ReporterList
        order_by = ('name')
        attrs = {
            'class': 'table table-striped table-bordered table-condensed'
        }


class StatsTable(tables.Table):
    name = tables.Column(verbose_name="Item")
    value = tables.Column(verbose_name="Value")
    details = tables.LinkColumn('reporters', verbose_name='Link for details')

    class Meta:
        attrs = {'class': 'table table-striped table-bordered table-condensed'}
