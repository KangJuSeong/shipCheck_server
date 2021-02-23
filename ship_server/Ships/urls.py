from django.conf.urls import url
from .views import (DetailNormalShipAPI, CreateNormalShipAPI, ListNormalShipAPI, SearchNormalShipAPI,
                    DetailWasteShipAPI, CreateWasteShipAPI, ListWasteShipAPI, LocationWasteShipAPI,
                    RemoveTrashData)

                    # NormalShipRegister, AllDelete, WasteShipReigster)

urlpatterns = [
    url(r'^ship/normal/(?P<pk>\d+)/$', DetailNormalShipAPI.as_view()),  # 일반 선박 세부 정보
    url(r'^ship/normal/create/', CreateNormalShipAPI.as_view()),  # 일반 선박 추가
    url(r'^ship/normal/list/', ListNormalShipAPI.as_view()),  # 일반 선박 목록  http://127.0.0.1:8000/Ships/ship/normal/list/?page=5
    url(r'^ship/normal/search/', SearchNormalShipAPI.as_view()),  # 일반 선박 검색
    url(r'^ship/waste/(?P<pk>\d+)/$', DetailWasteShipAPI.as_view()),  # 유기,폐 선박 세부 정보
    url(r'^ship/waste/create/', CreateWasteShipAPI.as_view()),  # 유기,폐 선박 추가
    url(r'^ship/waste/list/', ListWasteShipAPI.as_view()),  # 유기,폐 선박 목록
    url(r'^ship/waste/location/', LocationWasteShipAPI.as_view()),  # 유기,폐 선박 좌표 요청
    url(r'^test/(?P<pk>\d+)/$', RemoveTrashData.as_view()),
    # url(r'^regitnormal/', NormalShipRegister.as_view()),
    # url(r'^del/', AllDelete.as_view()),
    # url(r'regitwaste/', WasteShipReigster.as_view()),
]