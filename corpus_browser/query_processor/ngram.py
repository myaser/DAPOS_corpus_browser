from query_processor import Operator


class NGram(Operator):

    def __init__(self, n, estimator=None):

        self._k = n - 1
        self.estimator = estimator

    def set_index(self, index):
        Operator.set_index(self, index)
        self.estimator.set_index(index)

    def prob(self, statement):
        # TODO: avoid floating points underflow
        result = 1
        for i in range(len(statement) - 1, -1, -1):
            token = statement[i]
            if i < self._k:
                history = statement[:i]
            else:
                history = statement[i - self._k: i]
            result *= self.estimator(token=token,
                                     history=history)
        return result

    def operate(self, query_result, tokens, *args, **kwargs):
        return self.prob(tokens)
