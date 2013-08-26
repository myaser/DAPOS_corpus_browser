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
#         import pdb; pdb.set_trace()
        index_entery = AuxiliaryIndex.objects.get_or_create(token=token)[0]
        AuxiliaryIndex.objects(id=index_entery.id).update_one(
                                              push_all__postings=postings_list)
#         index_entery.postings += postings_list
#         index_entery.save()


@periodic_task(run_every=crontab(day_of_week="6", hour="13"), enabled=True)
def merge_index():
    '''
    weekly task that merges AuxiliaryIndex into MainIndex
    '''
    AuxiliaryIndex.merge(MainIndex)
