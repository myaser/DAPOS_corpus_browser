import os

from django.utils import unittest
from django.test import TestCase

from utils import change_collection
from indexer.models import AuxiliaryIndex, Tweet


def suite():
    suite = unittest.TestLoader()
    tests = suite.discover(os.path.dirname(__file__))
    return tests


@change_collection('test_Index')
class TestIndex(AuxiliaryIndex):
    pass


@change_collection('test_tweet')
class TestTweet(Tweet):
    pass


class MongoTestCase(TestCase):
    def tearDown(self):
        TestTweet.objects.delete()
        TestIndex.objects.delete()
        TestCase.tearDown(self)
