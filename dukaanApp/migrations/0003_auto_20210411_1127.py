# Generated by Django 3.0.6 on 2021-04-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dukaanApp', '0002_auto_20210411_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
