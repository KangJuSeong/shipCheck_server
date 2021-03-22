from django.conf.urls import url
from .views import NoticeAPI, QuestionAPI, AnswerAPI, QuestionCreateAPI, QuestionListAPI, NoticeListAPI


urlpatterns = [
    url(r'^notice/(?P<pk>\d+)/$', NoticeAPI.as_view()),
    url(r'^notice/list/', NoticeListAPI.as_view()),
    url(r'^question/(?P<pk>\d+)/$', QuestionAPI.as_view()),
    url(r'^answer/(?P<pk>\d+)/$', AnswerAPI.as_view()),
    url(r'^question/create/', QuestionCreateAPI.as_view()),
    url(r'^question/list/', QuestionListAPI.as_view())
]
