from Accounts.models import Account
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings

User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'rank', 'position', 'belong',
                  'phone', 'device_id', 'serviceNum')


class LoginSerializer(serializers.Serializer):
    serviceNum = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    device_id = serializers.CharField(max_length=255)

    def validate(self, data):
        serviceNum = data.get("serviceNum", None)
        password = data.get("password", None)
        device_id = data.get("device_id", None)
        # 유저 인증 성공시 user모델을 가져오고 실패시 user에 None이 들어감
        user = authenticate(serviceNum=serviceNum, password=password)
        if user is None:
            return {'message': "None"}
        else:
            if not (user.device_id == device_id):
                return {'message': "Device mismatch"}
            if user.is_waiting:
                print("Waiting for login approval")
                return {'message': 'Wating'}
            if user.is_blocked:
                print("Blocked Users")
                return {'message': 'Blocked'}
            else:
                print("Login Success! Hello " + user.name)
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                return {
                    'message': 'Success Login',
                    'serviceNum': user.serviceNum,
                    'token': jwt_token,
                    'device_id': user.device_id
                }