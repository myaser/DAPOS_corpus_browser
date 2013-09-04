from query_processor import Operator


class Collocationer(Operator):

    supported_scoring_algorithms = {
    '': ''
    }

    def __init__(self, scoring_algorithm=''):
        pass

    def operate(self, queryset):
        pass


class Scorer(object):
    def calc(self):
        pass
