from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views import static


urlpatterns = [
    
    url(r'^', include('collection.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG: 
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static.serve, { 
            'document_root': settings.MEDIA_ROOT,
        }),
    ]