from django.test import TestCase
from indexer.models import AuxiliaryIndex
import os
from corpus_browser.settings import PROJECT_ROOT


class IndexTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        fixture_file = os.path.join(PROJECT_ROOT, 'indexer/fixtures/testindex.json')
        fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(fixture)

    def test_target_documents(self):
        AuxiliaryIndex.objects.get(id='521b0cd2c454fe116c319878')
        pass

    def test_creation(self):
        pass

    def test_frequencies(self):
        pass

    def test_merge(self):
        pass
