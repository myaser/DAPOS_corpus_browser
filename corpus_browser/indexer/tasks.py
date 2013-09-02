import datetime

from celery.task.schedules import crontab
from celery.task import periodic_task

from indexer.models import Tweet, AuxiliaryIndex, Posting, MainIndex


@periodic_task(run_every=crontab(hour="1"), enabled=True)
def build_index():
    '''
    daily task that indexes all Tweet objects from yesterday into AuxiliaryIndex
    '''
    # TODO: performance optimization
    yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
    indexed_tweets = Tweet.objects.index(created_at__gte=yesterday)

    for token, postings in indexed_tweets.items():
        postings_list = [Posting(document=Tweet.objects.get(id=doc_id), positions=pos)
                         for doc_id, pos in postings.items()]
        AuxiliaryIndex.objects.add_postings(token, postings_list)


@periodic_task(run_every=crontab(day_of_week="6", hour="13"), enabled=True)
def merge_index():
    '''
    weekly task that merges AuxiliaryIndex into MainIndex
    '''
    AuxiliaryIndex.merge(MainIndex)
