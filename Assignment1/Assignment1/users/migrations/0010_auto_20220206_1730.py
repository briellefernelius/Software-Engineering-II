# Generated by Django 2.2 on 2022-02-07 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userimage',
            old_name='userid',
            new_name='user',
        ),
    ]