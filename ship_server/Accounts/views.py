import time
from utils.custom_view import APIView
from utils.change_format import change_unit
from .models import Account
from .serializers import LoginSerializer, AccountSerializer
from rest_framework.permissions import AllowAny
from utils.check_pw import check_pw
import logging
from django.core.exceptions import ObjectDoesNotExist
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import os


logger = logging.getLogger(__name__)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            logger.debug('Login Fail : {0}, Body : {1}'.format('데이터 오류', request.data))
            return self.fail(message="Request Body Error.")
        if serializer.validated_data['message'] == 'None':
            logger.debug('Login Fail : {}'.format('가입되지 않은 유저'))
            return self.fail(message="Unauthenticated user")
        if serializer.validated_data['message'] == 'Wating':
            logger.debug('Login Fail : {0} (군번 : {1})'.format('승인되지 않은 유저', request.data['srvno']))
            return self.fail(message="Waiting for login approval")
        if serializer.validated_data['message'] == 'Not connected 3months':
            logger.debug('Login Fail : {0} (군번 : {1})'.format('3달간 미접속 유저', request.data['srvno']))
            return self.fail(message="Not connected 3months Blocked user")
        if serializer.validated_data['message'] == 'Login fail blocked':
            logger.debug('Login Fail : {0} (군번 : {1})'.format('계정 정지 유저', request.data['srvno']))
            return self.fail(message='Login fail Blocked user')
        if serializer.validated_data['message'] == "Device mismatch":
            logger.debug('Login Fail : {0} (군번 : {1})'.format('등록되지 않은 디바이스', request.data['srvno']))
            return self.fail(message="Device mismatch")
        if serializer.validated_data['message'] == 'Incorrect password':
            logger.debug('Login Fail : {0} (군번 : {1})'.format('비밀번호 불일치', request.data['srvno']))
            return self.fail(message="Incorrect password")
        user = Account.objects.get(srvno=request.data['srvno'])
        logger.debug('Login Success : {0} ({1})'.format(user.srvno, user.name))
        return self.success(data={'token': serializer.data['token']}, message='Login Success')


class LogoutAPI(APIView):
    def get(self, request):
        if request.user is not None:
            logger.debug('Logout Success : {0} ({1})'.format(request.user.srvno, request.user.name))
            return self.success(message='Logout Success')
        else:
            logger.debug('Logout Fail : {0} (군번 : {1})'.format('None token', request.data['srvno']))
            return self.fail(message='None logged in')


class SignUpAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if Account.objects.filter(srvno=request.data['srvno']):
            logger.debug('Signup Fail : {0} (군번 : {1})'.format('이미 존재하는 계정', request.data['srvno']))
            return self.fail(message="Already exist serviceNum")
        if Account.objects.filter(device_id=request.data['device_id']):
            logger.debug('Signup Fail : {0} (군번 : {1})'.format('이미 등록된 단말기', request.data['device_id']))
            return self.fail(message="Already regist device")
        value = check_pw(request.data['password'])
        if value['status'] == '4':
            Account.objects.create_user(srvno=request.data['srvno'],
                                        password=request.data['password'],
                                        name=request.data['name'],
                                        rank=request.data['rank'],
                                        unit=request.data['unit'],
                                        position=request.data['position'],
                                        phone=request.data['phone'],
                                        device_id=request.data['device_id'])
            logger.debug('Signup Success : {0} (군번 : {1})'.format('회원가입 성공', request.data['srvno']))
            return self.success(message=value['message'])
        elif value['status'] == '3':
            logger.debug('Signup Fail : {0} (군번 : {1})'.format('비밀번호 조건 불충족', request.data['srvno']))
            return self.fail(message=value['message'])
        elif value['status'] == '2':
            logger.debug('Signup Fail : {0} (군번 : {1})'.format('비밀번호 조건 불충족', request.data['srvno']))
            return self.fail(message=value['message'])
        else:
            logger.debug('Signup Fail : {0} (군번 : {1})'.format('비밀번호 조건 불충족', request.data['srvno']))
            return self.fail(message=value['message'])


class UserInfoAPI(APIView):
    def get(self, request):
        try:
            user = Account.objects.get(id=self.request.user.id)
            serializer = AccountSerializer(user)
            result = change_unit(serializer.data)
            logger.debug('User Info Success : {0} (군번 : {1})'.format('유저 정보 불러오기', user.srvno))
            return self.success(result, message='success')
        except Exception as e:
            logger.debug('User Info Fail : {0}(에러 내용: {1})'.format('유저 정보 불러오기 실패', e))
            return self.fail(message='Not loading user information')


class UserPermissionAPI(APIView):
    def get(self, request):
        try:
            user = Account.objects.get(id=self.request.user.id)
            level = user.user_level
            logger.debug('User Permission Success : {0} (군번 : {1})'.format('유저 권한 불러오기', user.srvno))
            return self.success(data={"user_level": level}, message='success')
        except Exception as e:
            logger.debug('User Permission Fail : {0}(에러 내용: {1})'.format('유저 권한 불러오기 실패', e))
            return self.fail(message='fail')


class VersionCheckAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        now_version = "v1.0.1"
        server_status = ["running", "checking"]
        return self.success(data={"version": now_version, "server_status": server_status[0]}, message='success')
