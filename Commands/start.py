from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"New user: {update.effective_user.first_name} {update.effective_user.last_name}!")

    greetings = f"Привет {update.effective_user.first_name}! " \
                f"Я умею делать некоторые лабораторки. Но для начала нужно познакомиться."

    fullname_request = "Напиши свое полное имя (ФИО), которое будет написано в титульнике:"
    variant_request = "Отлично! Теперь мне нужен номер твоего варианта:"

    await update.message.reply_text(greetings)
    await update.message.reply_text(fullname_request)
    await update.message.reply_text(variant_request)
