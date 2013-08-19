import os
from django.utils import unittest
from django.utils.unittest.suite import TestSuite


def suite():
    suite = unittest.TestLoader()
    tests = suite.discover(os.path.dirname(__file__))
    return tests
