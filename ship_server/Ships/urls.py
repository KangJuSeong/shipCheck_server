from django.conf.urls import url
from .views import (DetailNormalShipAPI, CreateNormalShipAPI, ListNormalShipAPI, SearchNormalShipAPI,
                    DetailWasteShipAPI, CreateWasteShipAPI, ListWasteShipAPI,)
                    # NormalShipRegister, AllDelete, WasteShipReigster)

urlpatterns = [
    url(r'^ship/normal/(?P<pk>\d+)/$', DetailNormalShipAPI.as_view()),
    url(r'^ship/normal/create/', CreateNormalShipAPI.as_view()),
    url(r'^ship/normal/list/', ListNormalShipAPI.as_view()),
    url(r'^ship/normal/search/', SearchNormalShipAPI.as_view()),
    url(r'^ship/waste/(?P<pk>\d+)/$', DetailWasteShipAPI.as_view()),
    url(r'^ship/waste/create/', CreateWasteShipAPI.as_view()),
    url(r'^ship/waste/list/', ListWasteShipAPI.as_view()),
    # url(r'^regitnormal/', NormalShipRegister.as_view()),
    # url(r'^del/', AllDelete.as_view()),
    # url(r'regitwaste/', WasteShipReigster.as_view()),
]