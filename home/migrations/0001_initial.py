# Generated by Django 3.2.7 on 2021-09-20 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coisa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=64)),
                ('dono', models.CharField(max_length=64)),
                ('cont', models.CharField(max_length=8)),
                ('desc', models.CharField(blank=True, max_length=256)),
                ('pub', models.BinaryField()),
            ],
        ),
    ]