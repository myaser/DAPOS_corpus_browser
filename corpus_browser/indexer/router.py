class MongoRouter(object):
    """
    A router to control all database operations on models using mongodb
    """
    mongo_apps = ['indexer']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.mongo_apps:
            return 'mongo_db'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.mongo_apps:
            return 'mongo_db'
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        """
        mongo db needs no sync, and its models should not be synced
        """
        if db == 'mongo_db' or model._meta.app_label in self.mongo_apps:
            return False

        return None
