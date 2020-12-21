import time
from utils.custom_view import APIView
from Accounts.models import Account
from Accounts.serializers import LoginSerializer
from rest_framework.permissions import AllowAny


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return self.fail(message="Request Body Error.")
        if serializer.validated_data['message'] == 'None':
            return self.fail(message="Unauthenticated user")
        if serializer.validated_data['message'] == 'Wating':
            return self.fail(message="Waiting for login approval")
        if serializer.validated_data['message'] == 'Blocked':
            return self.fail(message="Blocked user")
        if serializer.validated_data['message'] == "Device mismatch":
            return self.fail(message="Device mismatch")
        response = {
            'token': serializer.data['token'],
        }
        message = 'Login Success'
        return self.success(data=response, message=message)


class LogoutAPI(APIView):
    def post(self, request):
        if request.user is not None:
            print('Logout Success Bye ' + request.user.name
                  + time.strftime('\nHistroy : %Y-%m-%d %H:%M:%S (%a)',
                                  time.localtime(time.time())))
            return self.success(message='Logout Success')
        else:
            return self.fail(message='None logged in')


class SignUpAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        Account.objects.create_user(serviceNum=request.data['serviceNum'],
                                    password=request.data['password'],
                                    name=request.data['name'],
                                    rank=request.data['rank'],
                                    belong=request.data['belong'],
                                    position=request.data['position'],
                                    phone=request.data['phone'],
                                    device_id=request.data['device_id'],)
        return self.success(message='Success Signup')


class SearchinPwAPI(APIView):
    def post(self, request):
        return self.success()


class DeleteUserAPI(APIView):
    def post(self, request):
        return self.success()