import time
from utils.custom_view import APIView
from Accounts.models import Account
from Accounts.serializers import LoginSerializer, AccountSerializer
from rest_framework.permissions import AllowAny
from utils.check_pw import check_pw


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return self.fail(message="Request Body Error.")
        if serializer.validated_data['message'] == 'None':
            print("Unauthenticated user")
            return self.fail(message="Unauthenticated user")
        if serializer.validated_data['message'] == 'Wating':
            print("Waiting for login approval")
            return self.fail(message="Waiting for login approval")
        if serializer.validated_data['message'] == 'Not connected 3months':
            print("Not connected 3months Blocked user")
            return self.fail(message="Not connected 3months Blocked user")
        if serializer.validated_data['message'] == 'Login fail blocked':
            print('Login fail Blocked user')
            return self.fail(message='Login fail Blocked user')
        if serializer.validated_data['message'] == "Device mismatch":
            print("Device mismatch")
            return self.fail(message="Device mismatch")
        if serializer.validated_data['message'] == 'Incorrect password':
            print("Incorrect password")
            return self.fail(message="Incorrect password")
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
        if Account.objects.filter(serviceNum=request.data['serviceNum']):
            return self.fail(message="Already exist serviceNum")
        if Account.objects.filter(device_id=request.data['device_id']):
            return self.fail(message="Already regist device")
        value = check_pw(request.data['password'])
        if value['status'] == '4':
            Account.objects.create_user(serviceNum=request.data['serviceNum'],
                                        password=request.data['password'],
                                        name=request.data['name'],
                                        rank=request.data['rank'],
                                        belong=request.data['belong'],
                                        position=request.data['position'],
                                        phone=request.data['phone'],
                                        device_id=request.data['device_id'])
            return self.success(message=value['message'])
        elif value['status'] == '3':
            return self.fail(message=value['message'])
        elif value['status'] == '2':
            return self.fail(message=value['message'])
        else:
            return self.fail(message=value['message'])


class UserInfoAPI(APIView):
    def post(self, request):
        user = Account.objects.get(id=self.request.user.id)
        serializer = AccountSerializer(user)
        return self.success(serializer.data, message='success')


class SearchingPwAPI(APIView):
    def post(self, request):
        return self.success()


class DeleteUserAPI(APIView):
    def post(self, request):
        return self.success()