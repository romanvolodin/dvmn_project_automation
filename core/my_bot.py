from datetime import datetime, date, time, timedelta
import logging
import time

import telegram
from telegram.ext import ConversationHandler

from core.models import ProductManager, Week, Student, Project, StudentProjectPreferences, TimeSlot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

REGISTRATION, WEEK, SLOT = range(3)


def start(bot, update):
    keyboard = [
        ['Зарегистрироваться!', 'Не, пока подумаю!']
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)

    update.message.reply_text(
        text='Привет! Если готов зарегистрироваться на проект, то жми "Зарегистрироваться"',
        reply_markup=reply_markup)
    return REGISTRATION


def register(bot, update):
    dates = [datetime.strftime(week.start_date, '%d-%m-%Y') for week in Week.objects.all()]
    keyboard = [
        dates, ['Без разницы!']
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text='Здорово, что решился! Рад, что ты с нами!')
    time.sleep(1)
    update.message.reply_text(
        text='Какого числа ты готов присоединиться к проекту?',
        reply_markup=reply_markup
    )
    return WEEK


def choose_week(bot, update):
    str_week_date = update.message.text
    tg_chat_id = update.message.chat.id
    student = Student.objects.get(tg_chat_id=tg_chat_id)
    project = Project.objects.first()
    if str_week_date == 'Без разницы!':
        student_week_preference = StudentProjectPreferences.objects.create(
            student=student,
            project=project,
            is_any_week=True
        )
    else:
        str_week_date_to_date = datetime.strptime(str_week_date, '%d-%m-%Y')
        week = Week.objects.get(start_date=str_week_date_to_date)
        student_week_preference = StudentProjectPreferences.objects.create(
            student=student,
            project=project,
            week=week
        )
    update.message.reply_text(text='Отлично, записал!')
    time.sleep(2)
    time_slots = []
    product_managers = ProductManager.objects.all()
    for product_manager in product_managers:
        slots = product_manager.pm_time_slots.all()
        for slot in slots:
            start_slot = datetime.combine(date.today(), slot.start)
            end_slot = datetime.combine(date.today(), slot.end)
            while start_slot <= end_slot:
                time_slots.append(start_slot)
                start_slot += timedelta(minutes=30)
    time_slots = sorted(list(set(time_slots)))
    time_slots_to_str = [datetime.strftime(time_slot, '%H:%M') for time_slot in time_slots]
    keyboard = [time_slots_to_str, ['В любое время!']]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(
        text='Выбери подходящие слоты для созвона с продукт-менеджером!',
        reply_markup=reply_markup)
    return SLOT


def choose_slot(bot, update):
    update.message.reply_text(
        text='Хорошо, записал! Если есть еще удобное время для созвона, то кликай по нему! Если закончил с выбором, то можешь нажать /cancel'
    )
    str_time_slot = update.message.text
    tg_chat_id = update.message.chat.id
    student = Student.objects.get(tg_chat_id=tg_chat_id)
    str_time_slot_to_strat_time = datetime.strptime(str_time_slot, '%H:%M')
    str_time_slot_to_end_time = str_time_slot_to_strat_time + timedelta(minutes=30)
    start_time = str_time_slot_to_strat_time.time()
    end_time = str_time_slot_to_end_time.time()
    time_slot = TimeSlot.objects.create(
        start=start_time, end=end_time
    )
    student_week_preference = StudentProjectPreferences.objects.get(student=student)
    student_week_preference.time_slots.add(time_slot)


def cancel(bot, update):
    update.message.reply_text(
        text='''Ну хорошо, подумай ещё! Только долго не затягивай! Как будешь готов, не забудь нажать заново кнопку /start :-)''')
    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
