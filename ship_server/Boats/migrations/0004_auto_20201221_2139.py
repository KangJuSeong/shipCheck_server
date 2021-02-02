# Generated by Django 2.2.4 on 2020-12-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boats', '0003_wasteboat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boat',
            old_name='boat_img',
            new_name='main_img',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='model_code',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='price',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='product_status',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='reserve',
        ),
        migrations.RemoveField(
            model_name='boat',
            name='title',
        ),
        migrations.AddField(
            model_name='boat',
            name='build_year',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='calsign',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='current_flag',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='home_port',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='imo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='is_learnig',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='boat',
            name='mmsi',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='boat',
            name='vessel_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='wasteboat',
            name='detail',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wasteboat',
            name='latitude',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wasteboat',
            name='longitude',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wasteboat',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]