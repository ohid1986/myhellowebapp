from django.conf.urls import url, include
from django.contrib import admin



urlpatterns = [
    
    url(r'^', include('collection.urls')),
    url(r'^admin/', include(admin.site.urls)),
]