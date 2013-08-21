from django.conf import settings


def template_variables(request):
    variables = {'BASE_DOMAIN': settings.ALLOWED_HOSTS[0]}
    try:
        # not present in dev settings, so ignore if absent
        variables.update({'SENTRY_URL': settings.SENTRY_URL})
    except AttributeError:
        pass
    return variables
