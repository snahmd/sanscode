# Generated by Django 5.0.7 on 2024-09-03 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogpage', '0003_ads'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ads',
            options={'verbose_name': 'Ad', 'verbose_name_plural': 'Ads'},
        ),
    ]