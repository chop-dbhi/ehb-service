from django.conf.urls import *
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
)
