from django.core.management.base import BaseCommand, CommandError
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

from backend.settings import TG_BOT_TOKEN
from core.my_bot import start, error, REGISTRATION, cancel, register, WEEK, choose_week, SLOT, choose_slot


class Command(BaseCommand):

    def handle(self, *args, **options):
        updater = Updater(TG_BOT_TOKEN)
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                REGISTRATION: [
                    MessageHandler(Filters.regex(r'Зарегистрироваться'),
                                   register),
                    MessageHandler(Filters.regex(r'Не, пока подумаю'), cancel)
                ],
                WEEK: [
                    MessageHandler(Filters.text, choose_week)
                ],
                SLOT: [
                    MessageHandler(Filters.text, choose_slot)
                ]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
        dp.add_handler(conv_handler)
        dp.add_error_handler(error)
        updater.start_polling()
        updater.idle()
