# Generated by Django 2.2 on 2022-02-02 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20220202_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('Computer Science', 'Computer Science'), ('Physics', 'Physics'), ('Math', 'Math'), ('English', 'English'), ('Engineering', 'Engineering')], default='', max_length=6)),
                ('course_number', models.CharField(max_length=20)),
                ('course_name', models.CharField(max_length=50)),
                ('credit_hours', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
    ]