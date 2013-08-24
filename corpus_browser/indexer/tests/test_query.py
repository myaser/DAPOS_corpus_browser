import os

from django.test import TestCase

from corpus_browser.settings import PROJECT_ROOT
from indexer.management.commands.loadcsvtweets import Command as LoadTweets
from indexer.tasks import build_index


class TestIndexQuerySet(TestCase):

    def setUp(self):
        TestCase.setUp(self)

    def test_queries(self):
        import pdb; pdb.set_trace()


