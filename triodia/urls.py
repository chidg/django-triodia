from django.conf.urls import patterns, url

urlpatterns = patterns(
    'triodia.views',
    url(r'^$', 'query_form', name='query_form'),

)
