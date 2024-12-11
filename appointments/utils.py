import datetime

from datetime import timedelta
from web import settings
from django.core.mail import send_mail

from .models import Appointment, Timetable, ClinicTime


def send_email_for_patient(email, appointment: Appointment):
    service_name = appointment.service if appointment.service else 'Не указана'

    send_mail(
        'Запись на прием',
        f'Вы записаны на прием к врачу: {appointment.doctor}\n'
        f'Дата: {appointment.date}\n'
        f'Время: {appointment.time}\n'
        f'Услуга: {appointment.service}\n'
        f'Цена: {appointment.price} сом\n',
        settings.EMAIL_HOST_USER,
        [email]
    )

def send_email_for_patient_update(email, appointment: Appointment):

    send_mail(
        'Изменения в записи на прием',
        f'Внесены изменения в записи на прием к врачу: {appointment.doctor}\n'
        f'Дата: {appointment.date}\n'
        f' Время: {appointment.time}\n'
        f'Услуга: {appointment.service}\n',
        settings.EMAIL_HOST_USER,
        [email]
    )


def days_of_week(date):
    days_of_week = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }

    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    day_of_week = date.weekday()

    return days_of_week[day_of_week]


def is_valid_appointment_time(appointment_time, doctor, appointment_date):
    errors = []

    day_of_week = appointment_date.weekday()

    timetable = Timetable.objects.filter(doctor=doctor, day_of_visit=day_of_week).first()

    if not timetable:
        errors.append(f"В выбранный день врач {doctor} не принимает пациентов.")
        return errors

    # Получаем время работы клиники
    clinic_time = ClinicTime.objects.first()

    if not clinic_time:
        errors.append("Не настроены часы работы клиники.")
        return errors

    if isinstance(appointment_time, str):
        appointment_time = datetime.datetime.strptime(appointment_time, "%H:%M").time()

    if not (clinic_time.work_start_time <= appointment_time <= clinic_time.work_end_time):
        errors.append(f"В выбранное время клиника не работает.")

    if clinic_time.lunch_start_time <= appointment_time < clinic_time.lunch_end_time:
        errors.append("Выбранное время попадает в обеденный перерыв.")

    if clinic_time.break_start_time <= appointment_time < clinic_time.break_end_time:
        errors.append("Выбранное время попадает в полдник.")

    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=appointment_date,
    )

    for appointment in existing_appointments:

        appointment_start_time = datetime.datetime.combine(appointment_date, appointment.time)
        appointment_end_time = appointment_start_time + timedelta(minutes=30)

        new_appointment_start = datetime.datetime.combine(appointment_date, appointment_time)

        print(f"Checking: New appointment time: {new_appointment_start}, Appointment start: {appointment_start_time}, Appointment end: {appointment_end_time}")

        if new_appointment_start < appointment_end_time and new_appointment_start + timedelta(minutes=30) > appointment_start_time:
            errors.append("Выбранное время пересекается с другой записью.")
            break

    return errors
