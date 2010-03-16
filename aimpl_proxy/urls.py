from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

from aimpl_proxy.aimpl.views import static

import os


static_pattern = patterns('aimpl_proxy.aimpl.views',
    url(r'^(.*)', 'static', name='static')
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('aimpl_proxy.registration.urls')),
    url(r'^pl$', include('aimpl_proxy.aimpl.urls')),
    url(r'^pl/', include('aimpl_proxy.aimpl.urls')),
    url(r'^aimpl/', static),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^jsMath/fonts/(?P<path>.*)$', 'django.views.static.serve', dict(
                document_root = os.path.join(settings.MEDIA_ROOT, 'jsMath', 'fonts'),
                show_indexes = True)
        ),
    )
    
urlpatterns += patterns('',
    url(r'^(.*)', include(static_pattern)),
)  
    
