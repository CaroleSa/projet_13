# Generated by Django 3.0.3 on 2020-03-03 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dietetic', '0009_auto_20200303_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionspace',
            name='robot_question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dietetic.RobotQuestion'),
        ),
    ]
