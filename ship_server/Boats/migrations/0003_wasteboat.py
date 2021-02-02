# Generated by Django 2.2.4 on 2020-12-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boats', '0002_auto_20201215_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='WasteBoat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.CharField(blank=True, max_length=100, null=True)),
                ('longitude', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]