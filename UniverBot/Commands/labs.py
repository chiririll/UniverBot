import math

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from UniverBot.Data import Labs, Query


class LabsCmd:
    __max_lines = 4
    __max_cols = 2

    @staticmethod
    async def subjects_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query

        await query.message.edit_text(f"Вот лабораторки по предмету \"{query.data}\"")

    @staticmethod
    def keyboard_generator(start: int = 0):
        keyboard = []

        keyboard.append([
            InlineKeyboardButton("Далее"),
            InlineKeyboardButton("Назад")
        ])

    @staticmethod
    def pack_data(data) -> str:
        return f"{Query.SelectSubject}:{data}"

    @staticmethod
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        subjects = Labs.get_subjects()

        start_index = 1

        cols = min(math.ceil(len(subjects) / LabsCmd.__max_lines), LabsCmd.__max_cols)
        count = min(cols * LabsCmd.__max_lines, len(subjects))

        keyboard = []

        for l in range(0, count, cols):
            line = []
            for i in range(l, min(count, l + cols)):
                line.append(InlineKeyboardButton(subjects[i].name, callback_data=f"{Query.SelectSubject}:{i}"))
            keyboard.append(line)

        last_line = []

        if start_index > 0:
            last_line.append(InlineKeyboardButton("< Назад", callback_data=f"{Query.SelectSubject}:next"))
        if count + start_index < len(subjects):
            last_line.append(InlineKeyboardButton("Далее >", callback_data=f"{Query.SelectSubject}:next"))

        keyboard.append(last_line)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Выбери предмет, который тебя интересует:", reply_markup=reply_markup)
