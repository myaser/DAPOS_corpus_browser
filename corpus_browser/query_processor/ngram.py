

class NGram():

    def __init__(self, n, index, estimator=None):

        self._k = n - 1
        self.index = index
        estimator.set_index(index)
        self.estimator = estimator

    def prob(self, statement):
        result = 1
        for i in range(len(statement) - 1, -1, -1):
            token = statement[i]
            if i < self._k:
                # heading empty strings
#                 history = [''] * (self._k - i) + statement[:i]
                history = statement[:i]
            else:
                history = statement[i - self._k: i]
            result *= self.estimator(token=token,
                                     history=history)
        return result
