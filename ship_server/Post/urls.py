from django.conf.urls import url
from .views import NoticeAPI


urlpatterns = [
    url(r'^notice/', NoticeAPI.as_view())
]
