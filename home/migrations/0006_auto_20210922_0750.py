# Generated by Django 3.2.7 on 2021-09-22 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20210922_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='coisa',
            name='email',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='coisa',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 22, 7, 50, 38, 1881)),
        ),
    ]