# Generated by Django 3.2.7 on 2021-09-22 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210922_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupocell',
            name='aproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coisa',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 22, 9, 9, 51, 904072)),
        ),
    ]
