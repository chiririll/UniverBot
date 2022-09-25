import json
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

        data = LabsCmd.unpack_data(query.data)

        if data.get('button_type', "") == "change_page":
            await LabsCmd.show_subjects(query.message, data.get('start', 0), True)
            return

        await query.message.edit_text(f"Вот лабораторки по предмету \"{query.data}\"")

    @staticmethod
    def keyboard_generator(names: list[str], data: list, start: int = 0) -> InlineKeyboardMarkup:
        keyboard = []

        names = names[start:]
        data = data[start:]

        cols = min(math.ceil(len(names) / LabsCmd.__max_lines), LabsCmd.__max_cols)
        count = min(cols * LabsCmd.__max_lines, len(names))

        for l in range(0, count, cols):
            line = []
            for i in range(l, min(count, l + cols)):
                line.append(InlineKeyboardButton(names[i], callback_data=LabsCmd.pack_data(data[i])))
            keyboard.append(line)

        last_line = []

        page_btn_data = {"button_type": "change_page"}
        if start > 0:
            page_btn_data["start"] = max(0, start - LabsCmd.__max_lines * LabsCmd.__max_cols)
            last_line.append(InlineKeyboardButton("< Назад", callback_data=LabsCmd.pack_data(page_btn_data)))
        if count < len(names):
            page_btn_data["start"] = count + start
            last_line.append(InlineKeyboardButton("Далее >", callback_data=LabsCmd.pack_data(page_btn_data)))

        keyboard.append(last_line)

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def pack_data(data: dict) -> str:
        return f"{Query.SelectSubject}:{json.dumps(data)}"

    @staticmethod
    def unpack_data(data: str) -> dict:
        parts = data.split(':', 1)
        if len(parts) < 2:
            return {}
        return json.loads(parts[1])

    @staticmethod
    async def show_subjects(message, start_index: int = 0, edit: bool = False) -> None:
        text = "Выбери предмет, который тебя интересует:"

        subjects = Labs.get_subjects()

        names = [subj.name for subj in subjects]
        data = [{} for i in range(len(subjects))]

        reply_markup = LabsCmd.keyboard_generator(names, data, start_index)

        if edit:
            await message.edit_text(text, reply_markup=reply_markup)
        else:
            await message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await LabsCmd.show_subjects(update.message)
