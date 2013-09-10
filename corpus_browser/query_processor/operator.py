class Operator(object):
    '''
    operator executed after query to do(concordance,OR collocation,OR N-gram)
    '''

    def operate(self):
        raise NotImplementedError()
