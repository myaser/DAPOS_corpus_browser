from celery import task
from indexer.models import Tweet, AuxilaryIndex, Posting
import datetime


@task
def build_index():
    try:
        yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
        recent_tweets = Tweet.objects.filter(created_at__gte=yesterday)
        indexed_tweets = recent_tweets.index()

        for row in indexed_tweets.items():
            postings_list = [Posting(document_id=doc_id, positions=pos)
                             for doc_id, pos in row[1].items()]
            AuxilaryIndex(token=row[0], postings=postings_list).save()
            # TODO: build merge functionality. token may be already in the Auxilary index
        return True
    except:
        return False
