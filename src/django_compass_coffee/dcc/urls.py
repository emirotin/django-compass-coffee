from django.conf.urls.defaults import *

urlpatterns = patterns('dcc.views',
    (r'^$', 'polls_index'),
    (r'^poll/(\d+)/vote/', 'poll_vote'),
    (r'^poll/(\d+)/results/', 'poll_results'),
    (r'^poll/(\d+)/', 'poll_view'),
    (r'^poll/create/', 'poll_create'),
)
