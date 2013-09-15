# Create your views here.
from django.shortcuts import render
from query_processor import QueryProcessor
from query_processor.probability import make_ngram_estimator
from query_processor.collocationer import Collocationer
from query_processor.ngram import NGram
from indexer.models import MainIndex


def main(request):
    return render(request, 'home.html', {'title': 'DAPOS'})


def _collocation(request):
    search_phrase = request.GET['search_phrase']
    scoring_algorithm = request.GET['collocation_algorithm']
    q = QueryProcessor(MainIndex, search_phrase, Collocationer(scoring_algorithm))
    collocations = q.excute_query()

    return render(request,
           'collocation.html',
           {'title': 'Collocation', 'collocations': collocations,
            'tokens': ' '.join(q.tokens), 'algorithm': scoring_algorithm}
        )


def _ngram(request):
    search_phrase = request.GET['search_phrase']
    estimator_str = request.GET['ngram_estimator']
    ngram_size = int(request.GET['ngram_size'])
    estimator = make_ngram_estimator(estimator_str)()
    q = QueryProcessor(MainIndex, search_phrase, NGram(ngram_size, estimator))
    ngrams = q.excute_query()

    return render(request,
            'ngrams.html',
            {'title': 'NGrams', 'ngrams': ngrams, 'search_phrase': search_phrase}
        )


def _concordance(request):
    search_phrase = request.GET['search_phrase']

    q = QueryProcessor(MainIndex, search_phrase)
    results, tokens = q.excute_query()

    return render(request,
                  'concordance.html',
                  {'title': 'Concordance',
                   'results':results,
                   'tokens': tokens,
                   'search_phrase': search_phrase}
                )


def _extract_process_type(request):
    try:
        print "here !"
        process = request.GET['process']
        return {
            'collocations': _collocation,
            'NGram': _ngram,
            'concordance': _concordance,
        }[process]
    except KeyError:
        # you should select process !
        raise ValueError('You choosed a wrong process!')


def search(request):
    process_func = _extract_process_type(request)
    # try:
    return process_func(request)
    # except KeyError:
    #     # damn selection error !!
    #     pass
