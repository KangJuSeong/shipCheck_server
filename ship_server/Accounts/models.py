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
            user.regit_date = datetime.today()
            user.last_login = datetime.now()
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)

    def create_superuser(self, srvno, password):
        try:
            superuser = self.create_user(
                srvno=srvno,
                password=password
            )
            superuser.is_active = True
            superuser.approve = True
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()
            return superuser
        except Exception as e:
            print(e)


UNIT_TYPE = [
    ('99-1', '99-1대대'),
    ('99-2', '99-2대대'),
    ('99-3', '99-3대대'),
    ('98-1', '98-1대대'),
    ('98-2', '98-2대대'),
    ('98-3', '98-3대대'),
    ('97-1', '97-1대대'),
    ('97-2', '97-2대대'),
    ('97-3', '97-3대대'),
    ('None', 'None')
]


class Account(AbstractBaseUser, PermissionsMixin):
    srvno = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=4, null=True, blank=True)
    rank = models.CharField(max_length=4, null=True, blank=True)
    position = models.CharField(max_length=20, null=True, blank=True)
    unit = models.CharField(max_length=4, choices=UNIT_TYPE, null=True,
                            blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    regit_date = models.DateField(null=True, blank=True)
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

    def __str__(self):
        return self.srvno

    db_table = 'Accounts'
