from utils.custom_view import APIView
from utils.change_datetime import change_datetime_notice
from .models import Notice, Question, Answer
from .serializers import NoticeSerializer, QuestionSerializer, AnswerSerializer


class NoticeAPI(APIView):
    def get(self, request):
        queryset = Notice.objects.all()
        serializer = NoticeSerializer(queryset, many=True)
        result = change_datetime_notice(data=serializer.data)
        return self.success(data=result, message='success')


class QuestionAPI(APIView):
    def get(self, request):
        queryset = Question.objects.filter(writer=request.user)
        serializer = QuestionSerializer(queryset, many=True)
        result = change_datetime_notice(data=serializer.data)
        return self.success(data=result, message='success')


class AnswerAPI(APIView):
    def get(self, request, pk=None):
        queryset = Answer.objects.get(q_id=pk)
        serializer = AnswerSerializer(queryset)
        result = change_datetime_notice(data=serializer.data)
        return self.success(data=result, message='success')



