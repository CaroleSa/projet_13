# Generated by Django 3.0.3 on 2020-03-08 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200305_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultsuser',
            name='weighing_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]