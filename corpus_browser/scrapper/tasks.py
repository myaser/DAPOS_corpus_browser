from celery.task.schedules import crontab
from celery.task import periodic_task
import models
from crawler import update_tweets


@periodic_task(run_every=crontab(minute="*/1"))
def lunch_crawlers(num_of_crawlers=3):
    seg_length = (models.Criterion.objects.count() / num_of_crawlers) + 1
    criteria = models.Criterion.objects.all()
    segmented_criteria = [criteria[seg:seg+seg_length] for seg in range(0, len(criteria), seg_length)]
    map(update_tweets.delay, segmented_criteria)
