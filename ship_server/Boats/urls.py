from django.conf.urls import url
from .views import DetailBoatAPI, SearchingBoatAPI, WasteBoatAPI, WasteDetailBoatAPI, test, RegistBoatAPI, PredictBoat, SearchingWastedAPI, ImageOfBoat, AddImage, DetailBoatImage


urlpatterns = [
    url(r'^boat/detail/', DetailBoatAPI.as_view()),
    url(r'^boat/searching/', SearchingBoatAPI.as_view()),
    url(r'^boat/regist/', RegistBoatAPI.as_view()),
    url(r'^test/', test.as_view()),
    url(r'^boat/wastedboats/', WasteBoatAPI.as_view()),
    url(r'^boat/detailwastedboat/', WasteDetailBoatAPI.as_view()),
    url(r'^boat/predict/', PredictBoat.as_view()),
    url(r'^boat/searchingwasted/', SearchingWastedAPI.as_view()),
    url(r'^boat/image/', ImageOfBoat.as_view()),
    url(r'^boat/addImage/', AddImage.as_view()),
    url(r'^boat/imagedetail/', DetailBoatImage.as_view())
]