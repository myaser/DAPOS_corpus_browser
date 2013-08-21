from indexer.models import Tweet, AuxiliaryIndex, Posting, MainIndex
import datetime
from django.db import transaction


# @task
def build_index():
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
        # TODO: logging
        return False


#@task
def merge_index():
    try:
        AuxiliaryIndex.merge(MainIndex)
        return True
    except Exception, e:
        # TODO: logging
        return False
