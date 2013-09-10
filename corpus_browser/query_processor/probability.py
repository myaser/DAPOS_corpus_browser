

class Estimator():
    # TODO: avoid underflow

    def __call__(self, token=None, history=None):
        raise NotImplementedError()

    def set_index(self, index):
        self.index = index
        self.index_size = index.get_index_size()
        self.num_tokens = index.get_tokens_count()

    def _get_count(self, counted):
        # we are counting documents not occurance in documents TODO: FIXME:
        if isinstance(counted, str):
            return self.index.objects.get(token=counted).term_frequency
        else:
            assert isinstance(counted, list)  # defensive programming
            if not counted:
                # count every thing
                return self.index_size
            elif len(counted) == 1:
                return self.index.objects.get(token=counted[0]).term_frequency
            else:
                return len(self.index.objects.consequent(token__in=counted))


class MLEEstimator(Estimator):  # maximum likelihood
    def __call__(self, token=None, history=None):
        count_history = self._get_count(history)

        joint_count = self._get_count(history + [token])
        try:
            prob = joint_count / float(count_history)
        except ZeroDivisionError:  # MLE can't estimate unknown tokens
            prob = 0.0
        return prob


class LidstoneEstimator(Estimator):  # add k smoothing
    def __init__(self, k):
        self._k = k

    def __call__(self, token=None, history=None):
        raise NotImplementedError()


class LaplaceEstimator(LidstoneEstimator):  # add one smoothing k=1
    def __init__(self):
        LidstoneEstimator.__init__(self, 1)


class ELEEstimator(LidstoneEstimator):  # expected likelihood k=0.5
    def __init__(self):
        LidstoneEstimator.__init__(self, 0.5)


class UnigramPriorEstimator(Estimator):
    def __call__(self, token=None, history=None):
        Estimator.__call__(self, token=token, history=history)

# from query_processor.ngram import NGram
# from query_processor.probability import *
# from indexer.models import *
# est = MLEEstimator()
# tri = NGram(3, AuxiliaryIndex, estimator=est)
