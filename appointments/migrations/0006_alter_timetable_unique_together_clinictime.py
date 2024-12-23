# Generated by Django 4.2.16 on 2024-12-10 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0005_alter_timetable_day_of_visit_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='ClinicTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], verbose_name='День недели')),
                ('work_start_time', models.TimeField(verbose_name='Начало рабочего дня')),
                ('work_end_time', models.TimeField(verbose_name='Конец рабочего дня')),
                ('lunch_start_time', models.TimeField(verbose_name='Начало обеда')),
                ('lunch_end_time', models.TimeField(verbose_name='Конец обеда')),
                ('break_start_time', models.TimeField(verbose_name='Начало полдника')),
                ('break_end_time', models.TimeField(verbose_name='Конец полдника')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Врач')),
            ],
            options={
                'verbose_name': 'Часы работы клиники',
                'verbose_name_plural': 'Часы работы клиники',
            },
        ),
    ]
