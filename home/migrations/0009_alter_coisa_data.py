# Generated by Django 3.2.7 on 2021-10-09 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210922_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coisa',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 9, 8, 35, 21, 429674)),
        ),
    ]
