# Generated by Django 3.0.3 on 2020-03-03 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietetic', '0007_auto_20200303_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotadvices',
            name='text',
            field=models.CharField(max_length=1700, unique=True),
        ),
    ]
