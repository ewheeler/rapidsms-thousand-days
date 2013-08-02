from django.conf.urls import url, patterns, include
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.template import add_to_builtins

add_to_builtins('avocado.templatetags.avocado_tags')

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/'), name='landing'),
    url(r'^query/', TemplateView.as_view(template_name='index.html'), name='query'),
    url(r'^results/', TemplateView.as_view(template_name='index.html'), name='results'),

    # Serrano-compatible Endpoint
    url(r'^api/', include('serrano.urls')),

    url(r'^patient/(?P<mrn>MRN\d+)/$', 'openmrs.views.patient_view', name='patient-detail'),
)
