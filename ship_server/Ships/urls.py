from django.conf.urls import url
from .views import DetailNormalShipAPI, CreateNormalShipAPI

urlpatterns = [
    url(r'^normalship/(?P<pk>\d+)/$', DetailNormalShipAPI.as_view()),
    url(r'^normalship/create/', CreateNormalShipAPI.as_view()),
]