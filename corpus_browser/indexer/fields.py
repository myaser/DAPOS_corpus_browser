from mongoengine.fields import ListField


class SetField(ListField):

    def to_python(self, value):
        return set(ListField.to_python(self, value))
