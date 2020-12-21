from django.conf.urls import url
from .views import GetDetailBoatAPI, GetSearchingBoatAPI, WasteBoatAPI, WasteDetailBoatAPI


urlpatterns = [
    url(r'^boat/detail/', GetDetailBoatAPI.as_view()),
    url(r'^boat/searching/', GetSearchingBoatAPI.as_view()),
    # url(r'^test/', test.as_view())
    url(r'^boat/wastedboats/', WasteBoatAPI.as_view()),
    url(r'^boat/detailwastedboat/', WasteDetailBoatAPI.as_view()),
]