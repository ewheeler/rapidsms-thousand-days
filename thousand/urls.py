from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from rapidsms.backends.kannel.views import KannelBackendView

import thousand

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    (r'^accounts/', include('rapidsms.urls.login_logout')),
    #url(r'^$', 'rapidsms.views.dashboard', name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    #(r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('rapidsms.contrib.registration.urls')),

    url(r'^$', 'thousand.views.index', name='rapidsms-dashboard'),
    url(r'^dashboard/$', 'thousand.views.dashboard'),
    (r'^nutrition/', include('nutrition.urls')),
    (r'^timelines/', include('timelines.urls')),
    (r'^xray/', include('xray.urls')),
    (r'^alerts/', include('alerts.urls')),
    (r'^groups/', include('groups.urls')),

    # Third party URLs
    (r'^selectable/', include('selectable.urls')),
    (r'^patients/', include('openmrs.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.INSTALLED_BACKENDS.get("kannel-yo"):
    urlpatterns + (url(r"^backend/kannel-yo/$",
                       KannelBackendView.as_view(backend_name="kannel-yo")),)
