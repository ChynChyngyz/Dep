from django.db import models


class Speciality(models.Model):
    DoesNotExist = None
    objects = None
    speciality_name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=30, blank=True)
    image = models.ImageField(upload_to='image_speciality/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return f'{self.speciality_name}'

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
