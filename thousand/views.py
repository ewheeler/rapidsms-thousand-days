from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    return render_to_response(
        "thousand/index.html",
        context_instance=RequestContext(request))

def dashboard(request):
    return render_to_response(
        "thousand/dashboard.html",
        context_instance=RequestContext(request))
