# Generated by Django 5.0.7 on 2024-08-11 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpage', '0017_subscribe_alter_blogdetail_body'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategories',
            name='category_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.customimage'),
        ),
    ]
