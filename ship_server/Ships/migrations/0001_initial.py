# Generated by Django 2.2.4 on 2021-02-11 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WasteShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.TextField(blank=True, null=True)),
                ('types', models.CharField(blank=True, max_length=10, null=True)),
                ('lat', models.FloatField(default=0)),
                ('lon', models.FloatField(default=0)),
                ('img_cnt', models.IntegerField(default=0)),
                ('is_train', models.BooleanField(default=False)),
                ('regit_date', models.DateTimeField(auto_now_add=True)),
                ('main_img', models.ImageField(blank=True, null=True, upload_to='waste_img/')),
                ('register', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waste_register', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WasteImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=0)),
                ('lon', models.FloatField(default=0)),
                ('regit_date', models.DateTimeField(auto_now_add=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='waste_add_img/')),
                ('register', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waste_add_register', to=settings.AUTH_USER_MODEL)),
                ('w_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waste_ship', to='Ships.WasteShip')),
            ],
        ),
        migrations.CreateModel(
            name='NormalShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
                ('port', models.CharField(blank=True, max_length=10, null=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('tons', models.FloatField(default=0)),
                ('types', models.CharField(blank=True, max_length=10, null=True)),
                ('is_vpass', models.BooleanField(default=False)),
                ('is_ais', models.BooleanField(default=False)),
                ('is_vhf', models.BooleanField(default=False)),
                ('is_ff', models.BooleanField(default=False)),
                ('img_cnt', models.IntegerField(default=0)),
                ('main_img', models.ImageField(blank=True, null=True, upload_to='normal_img/')),
                ('is_train', models.BooleanField(default=False)),
                ('regit_date', models.DateTimeField(auto_now_add=True)),
                ('register', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='normal_register', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NormalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='normal_add_img/')),
                ('regit_date', models.DateTimeField(auto_now_add=True)),
                ('n_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='normal_ship', to='Ships.NormalShip')),
                ('register', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='noraml_add_register', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]