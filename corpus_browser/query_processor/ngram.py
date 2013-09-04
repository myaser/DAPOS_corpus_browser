from query_processor import Operator
from nltk.model.ngram import NgramModel


class NGram(Operator):

    def __init__(self, n, estimator=None, *estimator_args, **estimator_kwargs):
        pass

    def operate(self, queryset):
        '''
        calculate the propability of phrase (from queryset)
        using language_model, estimate_method from initializer
        '''
        pass
