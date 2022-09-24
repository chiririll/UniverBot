from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from Enums import UserData
from .base_state import BaseState


class InitState(BaseState):

    states = ["get_fullname", "get_group", "get_variant"]

    def __init__(self, step: int = 0, update: Update = None, context: ContextTypes.DEFAULT_TYPE = None):
        self.step = step

        self.update = update
        self.context = context

    def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.update = update
        self.context = context

    def __request_fullname(self) -> None:
        self.update.message.reply_text(
            "Напиши свое полное имя (ФИО), которое будет написано в титульнике:"
        )

    def __request_group(self) -> None:
        self.update.message.reply_text(
            "Отлично, теперь отправь мне свою группу (Например: СИБ201):"
        )

    def __request_variant(self) -> None:
        self.update.message.reply_text(
            "И последнее, отправь мне номер своего варианта:"
        )

    def __finale(self) -> None:
        student = self.context.user_data.get(UserData.StudentInfo)

        if info is None:
            logger.critical(f"Student info is null! user data: {self.context.user_data}")
            self.update.message.reply_text("Произошла критическая ошибка!")
            return

        self.update.message.reply_text(
            "Все, теперь я запомнил твои данные и их не надо будет каждый раз вводить заново.\n"
            "Давай проверим:\n"
            f"ФИО: {}"
        )
