import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler
from loguru import logger

import Commands
from UniverBot import Enums, Conversations


def start():
    logger.info("Starting bot...")

    app = ApplicationBuilder().token(os.environ.get("TOKEN")).build()

    # Commands
    app.add_handler(CommandHandler(Enums.Command.Start, Commands.start_handler))
    app.add_handler(CommandHandler(Enums.Command.Subjects, Commands.subjects_handler))

    # Conversations
    app.add_handler(Conversations.build_student_data_handler())

    # Messages
    # app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bot started!")

    app.run_polling()


if __name__ == "__main__":
    start()
