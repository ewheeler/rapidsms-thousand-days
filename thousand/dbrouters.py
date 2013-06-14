

class OpenmrsRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'openmrs':
            return 'patients'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'openmrs':
            return 'patients'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'openmrs' or \
           obj2._meta.app_label == 'openmrs':
           return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'patients':
            return model._meta.app_label == 'openmrs'
        elif model._meta.app_label == 'openmrs':
            return False
        return None


class AvocadoRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'avocado':
            return 'patients'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'avocado':
            return 'patients'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'avocado' or \
           obj2._meta.app_label == 'avocado':
           return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'patients':
            return model._meta.app_label == 'avocado'
        elif model._meta.app_label == 'avocado':
            return False
        return None


class SerranoRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'serrano':
            return 'patients'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'serrano':
            return 'patients'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'serrano' or \
           obj2._meta.app_label == 'serrano':
           return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'patients':
            return model._meta.app_label == 'serrano'
        elif model._meta.app_label == 'serrano':
            return False
        return None


class CilantroRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'cilantro':
            return 'patients'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'cilantro':
            return 'patients'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'cilantro' or \
           obj2._meta.app_label == 'cilantro':
           return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'patients':
            return model._meta.app_label == 'cilantro'
        elif model._meta.app_label == 'cilantro':
            return False
        return None

