from django.conf.urls import url
from .views import NoticeAPI, QuestionAPI, AnswerAPI


urlpatterns = [
    url(r'^notice/', NoticeAPI.as_view()),
    url(r'^question/', QuestionAPI.as_view()),
    url(r'^answer/(?P<pk>\d+)/$', AnswerAPI.as_view())
]
