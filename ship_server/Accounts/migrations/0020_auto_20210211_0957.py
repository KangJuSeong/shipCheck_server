# Generated by Django 2.2.4 on 2021-02-11 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0019_auto_20210211_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='regit_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
