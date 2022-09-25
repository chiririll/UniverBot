from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from UniverBot.Data import Command


class StartCmd:
    @staticmethod
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.info(f"New user: {update.effective_user.first_name} {update.effective_user.last_name}!")

        greetings = f"Привет {update.effective_user.first_name}! " \
                    f"Я умею делать некоторые лабораторки.\n" \
                    f"\n" \
                    f"Вот список команд, которые могут тебе пригодиться:\n" \
                    f"/{Command.EditData} - редактировать данные (ФИО, вариант)\n" \
                    f"/{Command.Labs} - список доступных лабораторок"

        await update.message.reply_text(greetings)
