# Generated by Django 2.2 on 2022-01-30 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_merge_20220129_1936'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Submission',
        ),
    ]