from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from timelines.models import ReporterList, TimelineSubscription, Occurrence
from .tables import ReporterTable, StatsTable
from django_tables2 import RequestConfig
#from rapidsms import settings
from django.conf import settings
from rapidsms.contrib.messagelog.models import Message
from rapidsms.models import Backend
from timelines.unicsv import UnicodeCSVWriter
from django.http import HttpResponse


def index(request):
    return render_to_response(
        "thousand/index.html",
        context_instance=RequestContext(request))


def dashboard(request):
    # put some of the stats in memcache
    bname = getattr(settings, 'PREFERED_BACKEND', 'message_tester')
    default_backend = Backend.objects.get(name=bname)
    num_reporters = ReporterList.objects.count()
    active_subs = TimelineSubscription.objects.filter(end=None).count()
    inactive_subs = TimelineSubscription.objects.exclude(end=None).count()
    sent_messages = Message.objects.filter(
        direction='O', connection__backend=default_backend).count()
    received_messages = Message.objects.filter(
        direction='I', connection__backend=default_backend).count()
    confirmed = Occurrence.objects.filter(status=1).exclude(completed=None).count()

    data = [
        {'name': 'Number of registered VHTs', 'value': num_reporters, 'details': '/reporters'},
        {'name': 'Number of active timeline subscriptions', 'value': active_subs},
        {'name': 'Number of inactive timeline subscriptions', 'value': inactive_subs},
        {'name': 'Number of messages sent so far', 'value': sent_messages},
        {'name': 'Number of messages received so far', 'value': received_messages},
        {'name': 'Number of confirmed visits', 'value': confirmed},
    ]

    stats = StatsTable(data, template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(stats)

    return render(
        request, "thousand/dashboard.html",
        {'stats': stats})


def reporters_list(request):
    reporter_list = ReporterTable(
        ReporterList.objects.all(),
        template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(reporter_list)
    return render(
        request, "thousand/reporters.html",
        {'reporter_list': reporter_list})


def reporterCsvList(request):
    table = ReporterTable(ReporterList.objects.all())
    RequestConfig(request).configure(table)

    columns = [x.title() for x in table.columns.names()]
    rows = [columns, ]
    for item in table.rows:
        cells = [x for x in item]
        row = []
        for cell in cells:
            row.append(cell)
        rows.append(row)

    response = HttpResponse(content_type='text/csv')
    content_disposition = 'attachment; filename=%s.csv' % 'reporters'
    response['Content-Disposition'] = content_disposition
    writer = UnicodeCSVWriter(response)
    writer.writerows(rows)
    return response
