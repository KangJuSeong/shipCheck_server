from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^Accounts/', include('Accounts.urls')),
    url(r'^Ships/', include('Ships.urls')),
    url(r'^Posts/', include('Post.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
