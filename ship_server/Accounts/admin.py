from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'serviceNum',
        'name',
        'rank',
        'position',
        'belong',
        'phone',
        'device_id'
    )

admin.site.register(Account, AccountAdmin)