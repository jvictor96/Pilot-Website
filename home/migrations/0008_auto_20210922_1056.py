# Generated by Django 3.2.7 on 2021-09-22 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210922_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='tag',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='coisa',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 22, 10, 56, 39, 42463)),
        ),
    ]