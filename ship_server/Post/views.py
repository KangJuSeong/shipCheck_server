from utils.custom_view import APIView
from utils.change_datetime import change_datetime_notice
from .models import Notice, Question, Answer
from .serializers import NoticeSerializer


class NoticeAPI(APIView):
    def get(self, request):
        queryset = Notice.objects.all()
        serializer = NoticeSerializer(queryset, many=True)
        result = change_datetime_notice(data=serializer.data)
        return self.success(data=result, message='success')



