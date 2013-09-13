from django.conf.urls import patterns, url

urlpatterns = patterns('browser.views',
   url('^$', 'main', name='home'),
   url('^search/', 'search', name='search')
)
