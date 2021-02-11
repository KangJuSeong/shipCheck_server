from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


class AccountManager(BaseUserManager):
    def create_user(self, srvno, password, name=None, rank=None, position=None,
                    unit=None, phone=None, device_id=None):
        try:
            user = self.model(
                srvno=srvno,
                name=name,
                rank=rank,
                position=position,
                unit=unit,
                phone=phone,
                device_id=device_id
            )
            user.last_login = datetime.now()
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)

    def create_superuser(self, serviceNum, password):
        try:
            superuser = self.create_user(
                serviceNum,
                password=password
            )
            superuser.is_active = True
            superuser.is_waiting = False
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()
            return superuser
        except Exception as e:
            print(e)


UNIT_TYPE = [
    ('X9-1', 'X9-1대대'),
    ('X9-2', 'X9-2대대'),
    ('X9-3', 'X9-3대대'),
    ('X8-1', 'X8-1대대'),
    ('X8-2', 'X8-2대대'),
    ('X8-3', 'X8-3대대'),
    ('X7-1', 'X7-1대대'),
    ('X7-2', 'X7-2대대'),
    ('X7-3', 'X7-3대대'),
    ('None', 'None')
]


class Account(AbstractBaseUser, PermissionsMixin):
    srvno = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=4, null=True, blank=True)
    rank = models.CharField(max_length=4, null=True, blank=True)  # 계급 선택
    position = models.CharField(max_length=20, null=True, blank=True)
    unit = models.CharField(max_length=4, choices=UNIT_TYPE, default='None')  # 소속부대 선택
    phone = models.CharField(max_length=11, null=True, blank=True)
    regit_date = models.DateField(default=datetime.today())
    device_id = models.CharField(max_length=255, null=True, blank=True)
    fail_cnt = models.IntegerField(default=0)
    block_no = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    approve = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'srvno'
    REQUIRED_FIELD = ['name', 'rank', 'position', 'unit', 'phone',
                      'device_id']


class Meta:
    def __str__(self):
        return self.phone

    db_table = 'Accounts'
