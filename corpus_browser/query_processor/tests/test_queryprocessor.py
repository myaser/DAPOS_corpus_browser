# -*- coding: UTF-8 -*-

from utils.tests import MongoTestCase
from query_processor import QueryProcessor
from indexer.models import MainIndex

class QueryProcessorTest(MongoTestCase):

    def test_parse_search(self):
        q = QueryProcessor(MainIndex, u'الله اكبر')
        self.assertEqual('boolean', q.query_type)
        self.assertEqual(0, q.window)
        self.assertEqual([u'الله', u'اكبر'], q.tokens)

        q2 = QueryProcessor(MainIndex, u'الله اكبر\\79')
        self.assertEqual('proximity', q2.query_type)
        self.assertEqual(79, q2.window)
        self.assertEqual([u'الله', u'اكبر'], q2.tokens)

        q3 = QueryProcessor(MainIndex, u'"الله اكبر"')
        self.assertEqual('phrase', q3.query_type)
        self.assertEqual(None, q3.window)
        self.assertEqual([u'الله', u'اكبر'], q3.tokens)
