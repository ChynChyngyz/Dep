# Generated by Django 4.2.16 on 2024-12-08 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0002_alter_service_unique_together_remove_service_doctor_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='service',
            unique_together={('doctor', 'title')},
        ),
        migrations.RemoveField(
            model_name='service',
            name='doctor',
        ),
        migrations.AddField(
            model_name='service',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL, verbose_name='Доктор'),
            preserve_default=False,
        ),
    ]