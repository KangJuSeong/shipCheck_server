from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, serviceNum, name=None, rank=None, position=None,
                    belong=None, phone=None, device_id=None, password=None):
        try:
            user = self.model(
                serviceNum=serviceNum,
                name=name,
                rank=rank,
                position=position,
                belong=belong,
                phone=phone,
                device_id=device_id
            )
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)

    def create_superuser(self, serviceNum, password=None):
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

# srvno, rank, name, unit(소속부대), position, phone, regit_date(등록일자), last_login, password, approve, is_active, is_superuser, device_id, fail_cnt, block_no
class Account(AbstractBaseUser, PermissionsMixin):
    serviceNum = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    rank = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    belong = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)
    attemp = models.IntegerField(default=0)
    blocked = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_waiting = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'serviceNum'
    REQUIRED_FIELD = ['name', 'rank', 'position', 'belong', 'phone',
                      'device_id']


class Meta:
    def __str__(self):
        return self.phone

    db_table = 'Accounts'
