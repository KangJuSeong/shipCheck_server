from django.conf.urls import url
from Accounts.views import *


urlpatterns = [
    url(r'^login/', LoginAPI.as_view()),
    url(r'^signup/', SignUpAPI.as_view()),
    url(r'^logout/', LogoutAPI.as_view()),
    url(r'^delete/', DeleteUserAPI.as_view()),
    url(r'^info/', UserInfoAPI.as_view()),
]