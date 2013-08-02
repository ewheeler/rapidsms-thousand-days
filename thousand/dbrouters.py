
# http://stackoverflow.com/a/7615627/979056
apps = (
    'openmrs',
    'serrano',
    'avocado',
    #'south',  # <<<---------------- Comment / Uncomment here
)

db_name = 'patients'


class PatientRouter(object):
    """A router to control all database operations on models from
    applications in apps"""

    def db_for_read(self, model, **hints):
        """Point all operations on apps models to db_name"""
        if model._meta.app_label in apps:
            return db_name
        return None

    def db_for_write(self, model, **hints):
        """Point all operations on apps models to db_name"""
        if model._meta.app_label in apps:
            return db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if a model in apps is involved"""
        if obj1._meta.app_label in apps or obj2._meta.app_label in apps:
            return True
        return None

    def allow_syncdb(self, db, model):
        """Make sure the apps only appears on the db_name db"""
        if db == db_name:
            return model._meta.app_label in apps
        elif model._meta.app_label in apps:
            return False
        return None
