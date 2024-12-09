# Медицинский центр

--------------------------

Сайт написан с помощью фреймворка Django с применением следующего стека:

PostgresSQL
Django
Templates
Auth
Git
ORM 
Docker

------------------------------------

## Приложения

1. authUser - приложение для пользователей и врачей, при регистрации пользователь указывает роль: пациент или врач. Создается общая модель User. Список врачей наполняет модератор с правами доступа is_staff или is_superuser. Врач это расширенная модель пользователя, с возможностью просматривать список своих записей приемов пациентов. 
2. speciality - приложение для специализации медицинских услуг. Объединяет медицинские услуги по направлениям диагностики, с возможностью вывода списка направлений диагностики, списка услуг по направлению.
3. services - приложение для медицинских услуг. Выводит список услуг, информацию о конкретной услуге.
4. appointments - приложение для записи на медицинскую услугу. Реализована запись на медицинскую услугу к определенному врачу, или с выбором врача из списка. Можно записаться только на свободное время у врача и только на рабочие дни врача, указанные в модели timetable. При запуске через Docker, автоматически запускается задача, которая отслеживает и меняет статусы записей с истекшим сроком давности)

------------------------------------

## Модели и поля

1. **CustomUser** - модель для работы с пользователем и доктором сайта 
    - nickname - поле никнейма
    - email - поле для ввода e-mail 
    - phone - поле для ввода телефона 
    - avatar - аватар пользователя (*необязательное*)
    - first_name - Имя пользователя
    - last_name - Фамилия пользователя
    - date_of_birth - День рождения (*необязательное*)
    - role - роль (пациент или доктор)
    - speciality - внешний ключ к специализации врача
    - education - образование врача
    - experience - стаж работы
    - description - описание врача

2. **Speciality** - модель для специализации направлений услуг.
    - speciality_name - название специализации
    - description - описание специализации
    - image - поле для добавления картинки
   
3. **Service** - модель медицинская услуга
    - title - название услуги
    - doctor - сам доктор (от authUser)
    - image - картинка для описания услуги
    - price - стоимость услуги
    - speciality - специализация услуги, внешний ключ, объединяющий услуги по специализации
    - description - описание услуги
   
4. **Timetable** - расписание работы врача.
    - day_of_visit - рабочие дни недели
    - doctor - внешний ключ к модели **Doctor** (*ManyToManyField*)
   
5. **Appointment** - модель записи к врачу.
    - user - внешний ключ к модели пациента
    - doctor - внешний ключ к модели врача (расширенная модель User)
    - service - внешний ключ к модели медицинской услуги
    - date - дата оказания услуги
    - time - время оказания услуги
    - data_created - дата и время создания заказа (*default: now*)
    - status_of_appointment - статус заказа, (WAITING, COMPLETED, CANCELLED)
    - price - стоимость услуги
   
------------------------------------ 