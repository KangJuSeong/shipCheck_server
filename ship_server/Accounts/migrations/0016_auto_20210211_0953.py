# Generated by Django 2.2.4 on 2021-02-11 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0015_auto_20210211_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='regit_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 11, 9, 52, 58, 628226)),
        ),
    ]
