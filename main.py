import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from loguru import logger

import Commands


def start():
    logger.info("Starting bot...")

    app = ApplicationBuilder().token(os.environ.get("TOKEN")).build()

    app.add_handler(CommandHandler("start", Commands.start))
    app.add_handler(CommandHandler("subjects", Commands.subjects))

    # app.add_handler(MessageHandler())

    logger.info("Bot started!")

    app.run_polling()


if __name__ == "__main__":
    start()
