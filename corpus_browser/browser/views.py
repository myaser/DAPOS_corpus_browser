from django.shortcuts import render
from query_processor import QueryProcessor
from query_processor.probability import make_ngram_estimator
from query_processor.collocationer import Collocationer
from query_processor.ngram import NGram
from indexer.models import MainIndex
from forms import SearchForm


import logging
logger = logging.getLogger()


def main(request):
    context = request.GET.dict()
    context.update(title='DAPOS', form=SearchForm())
    return render(request, 'home.html', context)


def _collocation(request, form):
    search_phrase = form.cleaned_data['search_phrase']
    scoring_algorithm = form.cleaned_data['collocation_algorithm']

    q = QueryProcessor(MainIndex, search_phrase, Collocationer(scoring_algorithm))
    collocations = q.excute_query()

    context = request.GET.dict()
    context.update(title='Collocation', collocations=collocations,
            tokens=' '.join(q.tokens), algorithm=scoring_algorithm)

    return render(request,
           'collocation.html',
           context
        )


def _ngram(request, form):
    search_phrase = form.cleaned_data['search_phrase']
    estimator_str = form.cleaned_data['ngram_estimator']
    ngram_size = form.cleaned_data['ngram_size']

    estimator = make_ngram_estimator(estimator_str)()
    q = QueryProcessor(MainIndex, search_phrase, NGram(ngram_size, estimator))
    ngrams = q.excute_query()

    context = request.GET.dict()
    context.update(title='NGrams',
                   ngrams=ngrams,
                   search_phrase=search_phrase)

    return render(request,
            'ngrams.html',
            context
        )


def _concordance(request, form):
    search_phrase = form.cleaned_data['search_phrase']

    q = QueryProcessor(MainIndex, search_phrase)
    results, tokens = q.excute_query()
    context = request.GET.dict()
    context.update(title='Concordance',
                   results=results,
                   tokens=tokens,
                   search_phrase=search_phrase)
    return render(request,
                  'concordance.html',
                  context
                )


def _extract_process_type(process):
    return {
        'collocations': _collocation,
        'NGram': _ngram,
        'concordance': _concordance,
    }.get(process)


def search(request):
    '''
        return the needed results
    '''
    form = SearchForm(request.GET)
    if form.is_valid():
        process_func = _extract_process_type(form.cleaned_data['process'])
        return process_func(request, form)

    logger.error(form.errors)
    context = request.GET.dict()
    context.update(title='DAPOS', form=form)
    return render(request, 'home.html', context)
