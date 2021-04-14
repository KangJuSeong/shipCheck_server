from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'srvno',
        'name',
        'rank',
        'position',
        'unit',
        'phone',
        'regit_date',
        'approve',
        'user_level',
        'block_no',


    )
    search_fields = ['srvno', 'name', 'phone']


admin.site.register(Account, AccountAdmin)