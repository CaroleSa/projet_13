# Generated by Django 3.0.3 on 2020-03-03 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dietetic', '0005_auto_20200303_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robotadvices',
            name='advices_to_user',
        ),
    ]