# Generated by Django 2.2.4 on 2020-12-11 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_auto_20201211_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='rank',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]