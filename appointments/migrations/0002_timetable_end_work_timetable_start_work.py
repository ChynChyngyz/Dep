# Generated by Django 4.2.16 on 2024-12-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='end_work',
            field=models.TimeField(default='17:00', verbose_name='Время окончания работы'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='start_work',
            field=models.TimeField(default='8:00', verbose_name='Время начала работы'),
        ),
    ]
