from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from UniverBot.Buttons import PagedKeyboard
from UniverBot.Data import Labs, Query


class LabsCmd:
    @staticmethod
    async def subject_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query

        data = PagedKeyboard.unpack_data(query.data)

        if data.get('button_type', "") == "change_page":
            await LabsCmd.show_subjects(query.message, data.get('start', 0), True)
            return

        await LabsCmd.show_labs(query.message, data.get('subject_id'), 0)

    @staticmethod
    async def lab_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass

    @staticmethod
    async def show_subjects(message, start_index: int = 0, edit: bool = False) -> None:
        text = "Выбери предмет, который тебя интересует:"

        subjects = Labs.get_subjects()

        names = [subj.name for subj in subjects]
        data = [{"subject_id": i} for i in range(len(subjects))]

        keyboard = PagedKeyboard(Query.SelectSubject, names, data)
        reply_markup = keyboard.generate(start_index)

        if edit:
            await message.edit_text(text, reply_markup=reply_markup)
        else:
            await message.reply_text(text, reply_markup=reply_markup)

    @staticmethod
    async def show_labs(message, subject_id: int, start_index: int = 0) -> None:
        subject = Labs.get_subject(subject_id)

        text = f"Вот лабораторки по предмету \"{subject.name}\":"

        labs = Labs.get_labs(subject_id)

        names = [lab.info.theme for lab in labs]
        data = [{"lab_id": i} for i in range(len(labs))]

        keyboard = PagedKeyboard(Query.SelectLab, names, data)
        keyboard.add_button(InlineKeyboardButton(
            "<< Вернуться",
            callback_data=keyboard.pack_data(Query.SelectSubject, {'button_type': "change_page", "start": 0})
        ))
        reply_markup = keyboard.generate(start_index)

        await message.edit_text(text, reply_markup=reply_markup)

    @staticmethod
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await LabsCmd.show_subjects(update.message)
