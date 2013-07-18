def run_raven(watcher, arbiter, hook_name):
    from django.core.management import call_command
    call_command('validate')
    return True
