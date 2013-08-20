from django.conf import settings


def additional_settings(request):
    additions = {'BASE_DOMAIN': settings.ALLOWED_HOSTS[0]}
    try:
        additions.update({'SENTRY_URL': settings.SENTRY_URL})
    except AttributeError:
        pass
    return additions
