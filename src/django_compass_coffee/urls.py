from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^polls/', include('dcc.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
