from .models import Account
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings
from datetime import datetime, timezone
# from django.conf import timezone


User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'rank', 'position', 'unit',
                  'phone', 'device_id', 'srvno')


class LoginSerializer(serializers.Serializer):
    srvno = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    device_id = serializers.CharField(max_length=255)

    def validate(self, data):
        srvno = data.get("srvno", None)
        password = data.get("password", None)
        device_id = data.get("device_id", None)
        # 유저 인증 성공시 user모델을 가져오고 실패시 user에 None이 들어감
        user = authenticate(srvno=srvno, password=password)
        if user is None:
            try:
                user_sub = User.objects.get(srvno=srvno)
                if user_sub.block_no == 2:
                    print('Login fail blocked')
                    return {'message': 'Login fail blocked'}
                if user_sub.fail_cnt < 3:
                    user_sub.fail_cnt = user_sub.fail_cnt + 1
                    user_sub.save()
                    if user_sub.fail_cnt == 3:
                        user_sub.fail_cnt = 0
                        user_sub.block_no = 2
                        user_sub.save()
                        print('Login fail blocked')
                        return {'message': 'Login fail blocked'}
                    print('Incorrect password')
                    return {'message': 'Incorrect password'}
            except User.DoesNotExist:
                print("None")
                return {'message': "None"}
        else:
            blank_day = (datetime.now() - user.last_login).days
            # blank_day = (timezone.now() - user.last_login).days
            if blank_day >= 90:
                user.block_no = 1
                user.last_login = timezone.now()
                user.save()
            if not (user.device_id == device_id):
                return {'message': "Device mismatch"}
            if not user.approve:
                print("Waiting for login approval")
                return {'message': 'Wating'}
            if user.block_no == 1:
                print("Not connected 3months")
                return {'message': 'Not connected 3months'}
            if user.block_no == 2:
                print("Login fail blocked")
                return {'message': "Login fail blocked"}
            else:
                print("Login Success! Hello " + user.name)
                user.last_login = datetime.now()
                user.fail_cnt = 0
                user.save()
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                return {
                    'message': 'Success Login',
                    'srvno': user.srvno,
                    'token': jwt_token,
                    'device_id': user.device_id
                }