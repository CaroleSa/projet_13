# Generated by Django 3.0.3 on 2020-03-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietetic', '0006_remove_robotadvices_advices_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotadvices',
            name='text',
            field=models.CharField(max_length=1700),
        ),
    ]
