# Generated by Django 2.2.4 on 2021-02-18 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ships', '0006_auto_20210218_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normalship',
            name='tons',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]