# -*- coding: utf-8 -*-
from django.test import TestCase
from scrapper import models, crawler, tasks


class DefaultTest(TestCase):
    def setup(self):
        models.Criterion.objects.create(type='hash_tag', value=u'مصر')
        models.Criterion.objects.create(type='hash_tag', value=u'وطن')
        models.Criterion.objects.create(type='hash_tag', value=u'سيناء')
        models.Criterion.objects.create(type='hash_tag', value=u'عرب')
        models.Criterion.objects.create(type='user_name', value=u'moemenology')
        models.Criterion.objects.create(type='user_name', value=u'Mah_Yaser')


class FetchTest(DefaultTest):
    pass
