from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField


class Posting(models.Model):

    doc_id = models.IntegerField()
    positions = ListField()

    @property
    def target_document(self):
        pass


class MainIndex(models.Model):

    token = models.CharField(max_length=10)
    postings = ListField(EmbeddedModelField('Posting'))

    @property
    def document_frequency(self):
        pass

    @property
    def term_frequency(self):
        pass

    @property
    def target_documents(self):
        pass


class AuxilaryIndex(MainIndex):

    def merge(self):
        pass
