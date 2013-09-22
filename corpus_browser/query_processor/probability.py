

class Estimator():

    def __call__(self, token=None, history=None):
        raise NotImplementedError()

    def set_index(self, index):
        self.index = index
        self.index_size = index.get_size()
        self.num_tokens = index.get_tokens_count()


class MLEEstimator(Estimator):  # maximum likelihood
    def __call__(self, token=None, history=None):

        if not history:
            history_count = self.index_size
        else:
            history_count = self.index.objects.frequency(history)

        joint_count = self.index.objects.frequency(history + [token])
        try:
            prob = self._prob(joint_count, history_count)
        except ZeroDivisionError:  # MLE can't estimate unknown tokens
            prob = 0.0
        return prob

    def _prob(self, joint_count, history_count):
        return joint_count / float(history_count)


class LidstoneEstimator(Estimator):  # add k smoothing
    def __init__(self, k=1):
        self._k = k

    def __call__(self, token=None, history=None):

        if not history:
            history_count = self.index_size
        else:
            history_count = self.index.objects.frequency(history)

        joint_count = self.index.objects.frequency(history + [token])

        return self._prob(joint_count, history_count)

    def _prob(self, joint_count, history_count):
        return (joint_count + self._k) / float(
                                       history_count + self.index_size)


class LaplaceEstimator(LidstoneEstimator):  # add one smoothing k=1
    def __init__(self):
        LidstoneEstimator.__init__(self, 1)


class ELEEstimator(LidstoneEstimator):  # expected likelihood k=0.5
    def __init__(self):
        LidstoneEstimator.__init__(self, 0.5)


class UnigramPriorEstimator(LidstoneEstimator):

    def __call__(self, token=None, history=None):
        self.prior = self.index.objects.frequency(token) / float(self.index_size)
        return LidstoneEstimator.__call__(self, token=token, history=history)

    def _prob(self, joint_count, history_count):
        return (joint_count + self._k * self.prior) / float(history_count + self._k)


def make_ngram_estimator(estimator):
    return {"MLEEstimator": MLEEstimator,
    "LidstoneEstimator": LidstoneEstimator,
    "LaplaceEstimator": LaplaceEstimator,
    "ELEEstimator": ELEEstimator,
    "UnigramPriorEstimator": UnigramPriorEstimator,}.get(estimator)

# from query_processor.ngram import NGram
# from query_processor.probability import *
# from indexer.models import *
# est = MLEEstimator()
# tri = NGram(3, AuxiliaryIndex, estimator=est)
