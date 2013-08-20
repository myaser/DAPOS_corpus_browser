from django.test import TestCase
from scrapper import models, crawler, tasks

class DefaultTest(TestCase):
    def setup(self):
        models.Criterion.create(type='hash_tag', value=u'مصر')
        models.Criterion.create(type='hash_tag', value=u'وطن')
        models.Criterion.create(type='hash_tag', value=u'سيناء')
        models.Criterion.create(type='hash_tag', value=u'عرب')
        models.Criterion.create(type='user_name', value=u'moemenology')
        models.Criterion.create(type='user_name', value=u'mah_yaser')


class FetchTest(DefaultTest):
    pass
