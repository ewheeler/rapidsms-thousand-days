def run_raven(watcher, arbiter, hook_name):
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", watcher.env["DJANGO_SETTINGS_MODULE"])
    from django.core.management import call_command
    call_command('validate')
    return True
