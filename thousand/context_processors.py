from django.conf import settings


def additional_settings(request):
    return {'BASE_DOMAIN': settings.ALLOWED_HOSTS[0]}
