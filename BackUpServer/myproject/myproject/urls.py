from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^mainserver/',include('mainserver.urls')),
    url(r'^backupserver/',include('backupserver.urls')),
#     url(r'^backupserver/',include('backupserver.urls')),
#     url(r'^$', RedirectView.as_view(url='/mainserver/savefile/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
