from django.conf.urls import url
from .views import (DetailNormalShipAPI, CreateNormalShipAPI, ListNormalShipAPI, SearchNormalShipAPI,
                    DetailWasteShipAPI, CreateWasteShipAPI, ListWasteShipAPI, LocationShipAPI,
                    SearchWasteShipAPI, ListNormalImageAPI, ListWasteImageAPI, AddWasteImageAPI,
                    AddNormalImageAPI, ProgramNormalShipAPI, ProgramWasteShipAPI, PredictShipAPI,
                    DownloadAPI, NormalShipRegister, WasteShipReigster)

urlpatterns = [
    url(r'^ship/normal/(?P<pk>\d+)/$', DetailNormalShipAPI.as_view()),  # 일반 선박 세부 정보
    url(r'^ship/normal/create/', CreateNormalShipAPI.as_view()),  # 일반 선박 추가
    url(r'^ship/normal/list/', ListNormalShipAPI.as_view()),  # 일반 선박 목록
    url(r'^ship/normal/search/', SearchNormalShipAPI.as_view()),  # 일반 선박 검색
    url(r'^ship/waste/(?P<pk>\d+)/$', DetailWasteShipAPI.as_view()),  # 유기,폐 선박 세부 정보
    url(r'^ship/waste/create/', CreateWasteShipAPI.as_view()),  # 유기,폐 선박 추가
    url(r'^ship/waste/list/', ListWasteShipAPI.as_view()),  # 유기,폐 선박 목록
    url(r'^ship/location/', LocationShipAPI.as_view()),  # 유기,폐 선박 좌표 요청
    url(r'^ship/waste/search/', SearchWasteShipAPI.as_view()),  # 유기,폐 선박 검색
    url(r'^image/normal/list/(?P<pk>\d+)/$', ListNormalImageAPI.as_view()),  #일반 선박 이미지 목록
    url(r'^image/waste/list/(?P<pk>\d+)/$', ListWasteImageAPI.as_view()),  # 유기,폐 선박 이미지 목록
    url(r'^image/normal/add/', AddNormalImageAPI.as_view()),  # 일반 선박 이미지 추가 등록
    url(r'^image/waste/add/', AddWasteImageAPI.as_view()),  # 유기,폐 선박 이미지 추가 등록
    url(r'^ship/normal/program/(?P<pk>\d+)/$', ProgramNormalShipAPI.as_view()),
    url(r'^ship/waste/program/(?P<pk>\d+)/$', ProgramWasteShipAPI.as_view()),
    url(r'^predict/', PredictShipAPI.as_view()),
    url(r'download/', DownloadAPI.as_view()),
    url(r'^test/normal/regist/', NormalShipRegister.as_view()),
    url(r'^test/waste/regist/', WasteShipReigster.as_view())
]