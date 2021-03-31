from rest_framework import serializers
from .models import Notice, Question, Answer
from Accounts.models import Account


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'types', 'date')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'content', 'date', 'status')


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'date', 'answer')
