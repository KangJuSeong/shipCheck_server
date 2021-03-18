from rest_framework import serializers
from .models import Notice, Question, Answer
from Accounts.models import Account


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'types', 'date')
