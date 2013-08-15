from django.db import models
from django.utils import simplejson as json


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return json.loads(value, use_decimal=True)

    def get_prep_value(self, value):
        if value is None:
            return value

        return json.dumps(value, use_decimal=True)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
