from django.conf.urls import patterns, include, url

urlpatterns = patterns('triodia.views',
    url(r'^$', 'query_form', name='query_form'),

)
