class WordpressRouter(object):
    """ Router to use mysql for wordpress access."""

    def db_for_read(self, model, **hints):
        """
        :type model: django.db.models.Model
        :rtype: str
        """
        if model._meta.app_label == 'wordpress':
            return 'wordpress'
        return None

    def db_for_write(self, model, **hints):
        """
        :type model: django.db.models.Model
        :rtype: str
        """
        if model._meta.app_label == 'wordpress':
            return 'wordpress'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        :type obj1: django.db.models.Model
        :type obj2: django.db.models.Model
        :rtype: str
        """
        if obj1._meta.app_label == 'wordpress' and obj2._meta.app_label == 'wordpress':
            return 'wordpress'
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        :type app_label: str
        :rtype: str
        """
        if app_label == 'wordpress':
            return db == 'wordpress'
        return None
