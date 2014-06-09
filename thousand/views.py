from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from timelines.models import ReporterList, MessagesList, Timeline, TimelineSubscription, Occurrence, MessageErrorLog
from .tables import ReporterTable, StatsTable, MessagesTable
#from django_tables2 import RequestConfig
from django_tables2_reports.config import RequestConfigReport as RequestConfig
from django.conf import settings
from rapidsms.contrib.messagelog.models import Message
from rapidsms.models import Backend
#from timelines.unicsv import UnicodeCSVWriter
#from django.http import HttpResponse
from django.core.cache import cache


def index(request):
    return render_to_response(
        "thousand/index.html",
        context_instance=RequestContext(request))


def dashboard(request):
    # put some of the stats in memcache
    bname = getattr(settings, 'PREFERED_BACKEND', 'message_tester')
    default_backend = Backend.objects.get(name=bname)
    num_reporters = ReporterList.objects.count()
    if not cache.get('mother_subs'):
        mother_subs = TimelineSubscription.objects.filter(
            end=None, timeline=Timeline.objects.get(
                name='ANC/PNC Advice')).distinct('pin').count()
        cache.set('mother_subs', mother_subs, 40)
    else:
        mother_subs = cache.get('mother_subs')

    if not cache.get('preg_subs'):
        preg_subs = TimelineSubscription.objects.filter(
            end=None, timeline=Timeline.objects.get(
                name='New pregancy/Antenatal Care Visits')).count()
        cache.set('preg_subs', preg_subs, 40)
    else:
        preg_subs = cache.get('preg_subs')

    if not cache.get('birth_subs'):
        birth_subs = TimelineSubscription.objects.filter(
            end=None, timeline=Timeline.objects.get(name='New Birth/Postnatal Care Visits')).count()
        cache.set('birth_subs', birth_subs, 40)
    else:
        birth_subs = cache.get('birth_subs')
    sent_messages = Message.objects.filter(
        direction='O', connection__backend=default_backend).count()
    received_messages = Message.objects.filter(
        direction='I', connection__backend=default_backend).count()
    confirmed = Occurrence.objects.filter(status=1).exclude(completed=None).count()

    data = [
        {'name': 'Number of registered VHTs', 'value': num_reporters, 'details': '/reporters'},
        {'name': 'Mothers registered for ANC/PNC advice', 'value': mother_subs, 'details': ''},
        {'name': 'Mothers registered for Pregancy/Antenatal Care Visits', 'value': preg_subs, 'details': ''},
        {'name': 'Mothers registered for Birth/Postnatal Care Visits', 'value': birth_subs, 'details': ''},
        {'name': 'Number of confirmed visits', 'value': confirmed, 'details': ''},
        {'name': 'Number of messages sent so far', 'value': sent_messages, 'details': '/outmessages'},
        {'name': 'Number of messages received so far', 'value': received_messages, 'details': '/inmessages'},
        {'name': 'Error Messages', 'value': '', 'details': '/errormessages'},
    ]

    stats = StatsTable(data, template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(stats)

    return render(
        request, "thousand/dashboard.html",
        {'stats': stats})


def reporters_list(request):
    table = ReporterTable(
        ReporterList.objects.all(),
        template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(table)
    return render(
        request, "thousand/reporters.html",
        {'table': table})


def incoming_messages(request):
    table = MessagesTable(
        MessagesList.objects.filter(direction='I'),
        template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(table)
    return render(
        request, "thousand/reporters.html",
        {'table': table})


def outgoing_messages(request):
    table = MessagesTable(
        MessagesList.objects.filter(direction='O'),
        template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(table)
    return render(
        request, "thousand/reporters.html",
        {'table': table})


def error_messages(request):
    error_msg_ids = MessageErrorLog.objects.all().values_list('message')
    table = MessagesTable(
        MessagesList.objects.filter(direction='I', id__in=error_msg_ids),
        template="django_tables2/bootstrap-tables.html")

    paginate = {"per_page": settings.PAGINATOR_OBJECTS_PER_PAGE}
    RequestConfig(request, paginate=paginate).configure(table)
    return render(
        request, "thousand/reporters.html",
        {'table': table})
