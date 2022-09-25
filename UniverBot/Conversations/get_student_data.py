from enum import Enum

from Word4Univer import FullName, StudentInfo, NamePattern
from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

from .. import Enums


class InitSubState(Enum):
    GetFullName = 0,
    GetGroup = 1,
    GetVariant = 2


class GetStudentData:

    messsages = {
        InitSubState.GetFullName:
            "Напиши свое полное имя (ФИО), которое будет написано в титульнике:",
        InitSubState.GetGroup:
            "Отлично, теперь отправь мне свою группу (Например: СИБ201):",
        InitSubState.GetVariant:
            "И последнее, отправь мне номер своего варианта:"
    }

    def __init__(self, update: Update = None, context: ContextTypes.DEFAULT_TYPE = None):
        self.sub_state = InitSubState.GetFullName
        self.student = StudentInfo()

        super().__init__(update, context)

    async def start(self):
        self.context.user_data[Enums.UserData.StudentInfo] = self.student

        await self.update.message.reply_text(self.messsages[self.sub_state])

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.update = update
        self.context = context

        match self.sub_state:
            case InitSubState.GetFullName:
                self.student.name = FullName(*NamePattern('SNP').parse_str(update.message.text))
                self.sub_state = InitSubState.GetGroup

            case InitSubState.GetGroup:
                self.student.group = update.message.text
                self.sub_state = InitSubState.GetVariant

            case InitSubState.GetVariant:
                self.student.variant = int(update.message.text)
                context.user_data[Enums.UserData.CurrentState] = DefaultState
                await self.__finale()
                return

        await self.update.message.reply_text(self.messsages[self.sub_state])

    async def __finale(self) -> None:
        student = self.context.user_data.get(Enums.UserData.StudentInfo)

        if student is None:
            logger.critical(f"Student info is null! user data: {self.context.user_data}")
            await self.update.message.reply_text("Произошла критическая ошибка!")
            return

        await self.update.message.reply_text(
            "Все, теперь я запомнил твои данные и их не надо будет каждый раз вводить заново.\n"
            "Давай проверим:\n"
            "\n"
            f"ФИО: {student.name}\n"
            f"Группа: {student.group}\n"
            f"Вариант: №{student.variant}\n"
            f"\n"
            f"Если данные введены не правильно, то их можно исправить командой /{Enums.Command.EditData}"
        )
