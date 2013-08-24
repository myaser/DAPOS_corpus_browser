from django.db import models
from indexer.query import TweetsQuerySet, IndexQuerySet


class TweetsManager(models.Manager):

    def get_query_set(self):
        return TweetsQuerySet(self.model, using=self._db)


class IndexManager(models.Manager):

    def get_query_set(self):
        return IndexQuerySet(self.model, using=self._db)
