# Generated by Django 4.0.2 on 2022-03-25 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_remove_submission_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
    ]
