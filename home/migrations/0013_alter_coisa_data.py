# Generated by Django 3.2.7 on 2021-10-09 23:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_coisa_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coisa',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 9, 20, 34, 37, 154957)),
        ),
    ]