from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Accounts/', include('Accounts.urls')),
    url(r'^Boats/', include('Boats.urls')),
    url(r'^get-token/', obtain_jwt_token),
    url(r'^get-verify/', verify_jwt_token),
    url(r'^get-refresh/', refresh_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)