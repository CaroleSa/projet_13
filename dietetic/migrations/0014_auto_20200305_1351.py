# Generated by Django 3.0.3 on 2020-03-05 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dietetic', '0013_auto_20200305_1342'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='discussionspace',
            unique_together={('user_answer', 'robot_question')},
        ),
    ]