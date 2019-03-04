from django.conf.urls import *
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=True)),
]
