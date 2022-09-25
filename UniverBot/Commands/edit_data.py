from telegram import Update
from telegram.ext import ContextTypes

from UniverBot import Enums, Conversations


async def edit_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = Conversations.InitState(update, context)
    context.user_data[Enums.UserData.CurrentState] = state

    await update.message.reply_text("Запускаю процедуру редактирования данных...")
    await state.start()
