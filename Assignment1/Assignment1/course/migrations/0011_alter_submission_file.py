# Generated by Django 4.0.2 on 2022-02-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_submission_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(blank=True, upload_to='file_submissions/'),
        ),
    ]
