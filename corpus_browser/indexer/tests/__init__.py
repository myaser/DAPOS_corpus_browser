import os

from django.utils import unittest
from django.test import TestCase

from utils import change_collection
from indexer.models import AuxiliaryIndex, Tweet, TestTweet, TestIndex


def suite():
    suite = unittest.TestLoader()
    tests = suite.discover(os.path.dirname(__file__))
    return tests


class MongoTestCase(TestCase):
    def tearDown(self):
        TestTweet.objects.delete()
        TestIndex.objects.delete()
        TestCase.tearDown(self)
