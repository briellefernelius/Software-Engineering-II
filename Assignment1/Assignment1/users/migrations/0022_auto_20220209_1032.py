# Generated by Django 2.2 on 2022-02-09 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20220209_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='expiration_date',
            field=models.DateTimeField(blank=True, default='', null=True),
        ),
    ]