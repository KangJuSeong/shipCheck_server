from django.conf.urls import url
from .views import DetailNoramlShipAPI

urlpatterns = [
    url(r'^normalship/detail', DetailNoramlShipAPI.as_view())
]