from utils.tests import MongoTestCase
import os
from corpus_browser.settings import PROJECT_ROOT
from indexer.models import AuxiliaryIndex, Tweet
from nltk.model.ngram import NgramModel
from nltk.probability import MLEProbDist, LaplaceProbDist, ELEProbDist
from query_processor.probability import MLEEstimator, LaplaceEstimator, ELEEstimator
from query_processor.ngram import NGram


class TestNGram(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testindex.json')
        self.index_fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(self.index_fixture)

        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testtweets.json')
        self.tweet_fixture = open(fixture_file).read()
        Tweet.load_data(self.tweet_fixture)

        self.corpus = [tweet.tokens for tweet in Tweet.objects]

    def test_segmentation(self):
        pass

    def test_MLEEstimator(self):
        est = MLEEstimator()
        dapos_model = NGram(3, estimator=est)
        dapos_model.set_index(AuxiliaryIndex)

        nltk_model = NgramModel(3, self.corpus, estimator=MLEProbDist)
        phrase = 'Stop being stunned'.split()
        x = dapos_model.prob(phrase)
        y = nltk_model.prob(phrase[2], phrase[:2])
#         import pdb; pdb.set_trace()

    def test_LaplaceEstimator(self):
        pass

    def test_ELEEstimator(self):
        pass

    def test_UnigramPriorEstimator(self):
        pass
