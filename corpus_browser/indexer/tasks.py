import datetime

from celery.task.schedules import crontab
from celery.task import periodic_task

from django.db import transaction

from indexer.models import Tweet, AuxiliaryIndex, Posting, MainIndex


@periodic_task(run_every=crontab(hour="1"), enabled=True)
def build_index():
    '''
    daily task that indexes all Tweet objects from yesterday into AuxiliaryIndex
    '''
    # TODO: performance optimization
    try:
        yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
        recent_tweets = Tweet.objects.filter(created_at__gte=yesterday)
        indexed_tweets = recent_tweets.index()
        with transaction.commit_on_success():
            for token, postings in indexed_tweets.items():
                postings_list = [Posting(document_id=doc_id, positions=pos)
                                 for doc_id, pos in postings.items()]
                index_entery = AuxiliaryIndex.objects.get_or_create(token=token)[0]
                index_entery.postings += postings_list
                index_entery.save()
        return True
    except Exception, e:
        print e
        # TODO: logging
        return False


@periodic_task(run_every=crontab(day_of_week="6", hour="13"), enabled=True)
def merge_index():
    '''
    weekly task that merges AuxiliaryIndex into MainIndex
    '''
    try:
        AuxiliaryIndex.merge(MainIndex)
        return True
    except Exception, e:
        # TODO: logging
        return False
