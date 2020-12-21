from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


User = get_user_model()


class APIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    @classmethod
    def raw_response(cls, content: dict, status: int = 200) -> JsonResponse:
        return JsonResponse(content, status=status)

    def response(self, data, message, status):
        return self.raw_response({'data': data, 'message': message, 'status': status}, status)

    def success(self, data=None, message='') -> JsonResponse:
        return self.response(data, message, 200)

    def fail(self, data=None, message='', status: int = 400) -> JsonResponse:
        return self.response(data, message, status)
