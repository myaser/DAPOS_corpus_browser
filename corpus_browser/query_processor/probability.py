

class Estimator():
    # TODO: avoid underflow

    def __call__(self, token=None, history=None):
        raise NotImplementedError()

    def set_index(self, index):
        self.index = index


class MLEEstimator(Estimator):  # maximum likelihood
    def __call__(self, token=None, history=None):
        # note: you are counting documents not occurance in documents
        count_history = len(self.index.objects.consequent(token__in=history))
        joint_count = len(self.index.objects.consequent(
                                            token__in=history.append(token)))
        return joint_count / float(count_history)


class LidstoneEstimator(Estimator):  # add k smoothing
    pass


class LaplaceEstimator(LidstoneEstimator):  # add one smoothing k=1
    pass


class ELEEstimator(LidstoneEstimator):  # expected likelihood k=0.5
    pass


class WittenBellEstimator(Estimator):  # wittenbell estimate
    pass


class GoodTuringEstimator(Estimator):
    def __init__(self):
        raise NotImplementedError()


class SimpleGoodTuringEstimator(Estimator):
    def __init__(self):
        raise NotImplementedError()
