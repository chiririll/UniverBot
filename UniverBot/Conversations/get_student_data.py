from enum import Enum

from Word4Univer import FullName, StudentInfo, NamePattern
from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters

from .. import Enums


class State:
    GetFullName = 0
    GetGroup = 1
    GetVariant = 2


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data[Enums.UserData.StudentInfo] = StudentInfo()

    await update.message.reply_text("Напиши свое полное имя (ФИО), которое будет написано в титульнике:")
    return State.GetFullName


async def __get_student(update: Update, context: ContextTypes.DEFAULT_TYPE) -> StudentInfo:
    student = context.user_data.get(Enums.UserData.StudentInfo)
    if student is None:
        await __student_null(update, context)
    return student


async def __student_null(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.critical(f"Student info is null! user data: {context.user_data}")
    await update.message.reply_text("Произошла критическая ошибка!")
    return


async def get_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    student = await __get_student(update, context)
    if student is None:
        return ConversationHandler.END

    student.name = FullName(*NamePattern('SNP').parse_str(update.message.text))

    await update.message.reply_text("Отлично, теперь отправь мне свою группу (Например: СИБ201):")
    return State.GetGroup


async def get_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    student = await __get_student(update, context)
    if student is None:
        return ConversationHandler.END

    student.group = update.message.text

    await update.message.reply_text("И последнее, отправь мне номер своего варианта:")
    return State.GetVariant


async def get_variant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    student = await __get_student(update, context)
    if student is None:
        return ConversationHandler.END

    try:
        student.variant = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Неправилиный формат варианта! Ожидается целое число.")
        return State.GetVariant

    return await __finale(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Ок, отменяю.")
    return ConversationHandler.END


async def __finale(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    student = await __get_student(update, context)
    if student is None:
        return ConversationHandler.END

    if student is None:
        await __student_null(update, context)

    await update.message.reply_text(
        "Все, теперь я запомнил твои данные и их не надо будет каждый раз вводить заново.\n"
        "Давай проверим:\n"
        "\n"
        f"ФИО: {student.name}\n"
        f"Группа: {student.group}\n"
        f"Вариант: №{student.variant}\n"
        f"\n"
        f"Если данные введены не правильно, то их можно исправить командой /{Enums.Command.EditData}"
    )

    return ConversationHandler.END


def build_student_data_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler('editdata', start)
        ],
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
        states={
            State.GetFullName: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fullname)],
            State.GetGroup: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_group)],
            State.GetVariant: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_variant)],
        }
    )
