from django.conf.urls import url
from .views import DetailNoramlShipAPI, CreateNormalShipAPI

urlpatterns = [
    url(r'^normalship/(?P<pk>\d+)/$', DetailNoramlShipAPI.as_view()),
    url(r'^normalship/create/', CreateNormalShipAPI.as_view()),
]