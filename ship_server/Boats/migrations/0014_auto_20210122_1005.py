# Generated by Django 2.2.4 on 2021-01-22 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boats', '0013_auto_20210121_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boatimg',
            name='add_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]