# -*- coding: UTF-8 -*-

from utils.string_processor import split_unicode

from django import template

register = template.Library()

@register.filter(name='highlight', is_safe=True)
def highlight(tweet, postions):
    tweet_tokens = split_unicode(tweet)
    marker = u"<strong>{word}</strong>"
    for token, postion in postions:
        for p in postion:
            tweet_tokens[p] = marker.format(word=token)

    return u" ".join(tweet_tokens)

