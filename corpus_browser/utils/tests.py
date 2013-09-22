from django.test import TestCase
from django.conf import settings

from mongoengine import connect, connection


class MongoTestCase(TestCase):

    """
    TestCase class that clear the collection between the tests
    """
    db_name = 'test_%s' % settings.MONGO_DATABASE_NAME

    def __init__(self, methodName='runtest'):
        connection.disconnect()
        connect(self.db_name)
        super(MongoTestCase, self).__init__(methodName)

    def _post_teardown(self):
        super(MongoTestCase, self)._post_teardown()
        for collection in connection.get_db().collection_names():
            if collection == 'system.indexes':
                continue
            connection.get_db().drop_collection(collection)
