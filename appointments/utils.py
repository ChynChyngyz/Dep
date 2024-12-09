import datetime

from django import forms

from web import settings
from django.core.mail import send_mail

from .models import Appointment, Timetable


def send_email_for_patient(email, appointment: Appointment):

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


def get_week_days(days):
    """
    Функция для получения рабочих дней недели врача.
    """
    days_dict = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    tmp_list = [days_dict.get(day) for day in days]
    return ', '.join(tmp_list)


# def check_doctor_service(doctor, service):
#
#     if doctor.speciality != service.speciality:
#         raise forms.ValidationError('Выбранная услуга не оказывается врачом')


def check_doctor_timetable_date(date, doctor):

    try:
        timetable = Timetable.objects.get(doctor=doctor, day_of_visit=date.weekday())
    except Timetable.DoesNotExist:
        raise forms.ValidationError(
            f'У врача нет приема в этот день. Рабочие дни: {get_week_days(doctor.timetable.all())}')

    if date <= datetime.date.today():
        raise forms.ValidationError(
            'Запись доступна только на завтра и далее. Вы не можете записаться на сегодня или в прошлое.')

    return timetable


def check_appointment_time(all_time, time, start_work, end_work):

    if start_work <= time <= end_work:
        if not all_time or min(all_time) >= datetime.time(start_work.hour + 1):
            next_free_time = start_work
        else:
            next_free_time = datetime.time(start_work.hour + 1)
            for cur_time in all_time:
                if datetime.time(cur_time.hour - 1, cur_time.minute) < next_free_time:
                    next_free_time = datetime.time(cur_time.hour + 1, cur_time.minute)
        if next_free_time >= end_work:
            raise forms.ValidationError('Записи на этот день нет. Выберите другую дату')
        for cur_time in all_time:
            if cur_time <= time < datetime.time(cur_time.hour + 1, cur_time.minute):
                raise forms.ValidationError(f'Время {time.strftime("%H:%M")} '
                                            f'уже занято. Ближайшее свободное время '
                                            f'{next_free_time.strftime("%H:%M")}')
    else:
        raise forms.ValidationError(f'Время работы клиники '
                                    f'с {start_work.strftime("%H:%M")} до {end_work.strftime("%H:%M")}')
