# Generated by Django 4.0.2 on 2022-02-26 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_usermessages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermessages',
            old_name='user',
            new_name='user_id',
        ),
    ]
