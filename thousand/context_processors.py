from django.conf import settings


def template_variables(request):
    """ Adds varialbes to template context """
    # BASE_DOMAIN is used to construct URLs to additional admin pages
    variables = {'BASE_DOMAIN': settings.ALLOWED_HOSTS[0]}
    try:
        # if sentry is installed, show link in admin menu
        # not present in dev settings, so ignore if absent
        variables.update({'SENTRY_URL': settings.SENTRY_URL})
    except AttributeError:
        pass
    try:
        # if statsd is installed, show link to graphite in admin menu
        # not present in dev settings, so ignore if absent
        variables.update({'STATSD_TRACK_MIDDLEWARE':
                          settings.STATSD_TRACK_MIDDLEWARE})
    except AttributeError:
        pass
    return variables
