from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

import Enums
from .base_state import BaseState

from Word4Univer.


class InitState(BaseState):

    states = ["get_fullname", "get_group", "get_variant"]

    def __init__(self, update: Update = None, context: ContextTypes.DEFAULT_TYPE = None):
        self.step = 0

        super().__init__(update, context)

    def start(self):
        self.context.user_data[Enums.UserData.StudentInfo] = ""

    def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.update = update
        self.context = context

    def __request_fullname(self) -> None:
        self.update.message.reply_text(
            "Напиши свое полное имя (ФИО), которое будет написано в титульнике:"
        )

    def __save_fullname(self):
        pass

    def __request_group(self) -> None:
        self.update.message.reply_text(
            "Отлично, теперь отправь мне свою группу (Например: СИБ201):"
        )

    def __request_variant(self) -> None:
        self.update.message.reply_text(
            "И последнее, отправь мне номер своего варианта:"
        )

    def __finale(self) -> None:
        student = self.context.user_data.get(Enums.UserData.StudentInfo)

        if student is None:
            logger.critical(f"Student info is null! user data: {self.context.user_data}")
            self.update.message.reply_text("Произошла критическая ошибка!")
            return

        # TODO
        self.update.message.reply_text(
            "Все, теперь я запомнил твои данные и их не надо будет каждый раз вводить заново.\n"
            "Давай проверим:\n"
            f"ФИО: {student.name}\n"
            f"Группа: {student.group}\n"
            f"Вариант: №{student.variant}\n"
            f"\n"
            f"Если данные введены не правильно, то их можно исправить командой /{Enums.Command.EditData}"
        )
