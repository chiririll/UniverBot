import os

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from loguru import logger

import Commands
from UniverBot import Data, Conversations


def start():
    logger.info("Starting bot...")

    app = ApplicationBuilder().token(os.environ.get("TOKEN")).build()

    # Commands
    app.add_handler(CommandHandler(Data.Command.Start, Commands.Start.handler))
    app.add_handler(CommandHandler(Data.Command.Labs, Commands.Labs.handler))

    # Buttons
    app.add_handler(CallbackQueryHandler(
        Commands.Labs.subject_button, pattern=f"{Data.Query.SelectSubject}:*"
    ))

    # Conversations
    app.add_handler(Conversations.build_student_data_handler())

    # Messages
    # app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("Bot started!")

    app.run_polling()


if __name__ == "__main__":
    start()
