from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from UniverBot import Enums, Conversations


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"New user: {update.effective_user.first_name} {update.effective_user.last_name}!")

    greetings = f"Привет {update.effective_user.first_name}! " \
                f"Я умею делать некоторые лабораторки. Но для начала нужно познакомиться."

    await update.message.reply_text(greetings)

    state = Conversations.InitState(update, context)
    context.user_data[Enums.UserData.CurrentState] = state
    await state.start()
