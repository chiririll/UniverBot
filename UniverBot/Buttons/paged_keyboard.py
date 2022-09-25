import json
import math

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from UniverBot.Data import Query


class PagedKeyboard:
    __max_lines = 6
    __max_cols = 2

    def __init__(self, query: Query, buttons_labels: list[str], buttons_data: list[dict]):
        self.query = query

        self.labels = buttons_labels
        self.data = buttons_data

        self.count = min(len(buttons_labels), len(buttons_data))

        self.service_buttons = []

    def __pack_data(self, data: dict) -> str:
        return f"{self.query}:{json.dumps(data)}"

    @staticmethod
    def pack_data(query: Query, data: dict):
        return f"{query}:{json.dumps(data)}"

    @staticmethod
    def unpack_data(data: str) -> dict:
        parts = data.split(':', 1)
        if len(parts) < 2:
            return {}
        return json.loads(parts[1])

    def generate(self, start: int = 0) -> InlineKeyboardMarkup:
        keyboard = []

        names = self.labels[start:]
        data = self.data[start:]

        cols = max(1, min(math.ceil(len(names) / self.__max_lines), self.__max_cols))
        count = min(cols * self.__max_lines, len(names))

        for l in range(0, count, cols):
            line = []
            for i in range(l, min(count, l + cols)):
                line.append(InlineKeyboardButton(names[i], callback_data=self.__pack_data(data[i])))
            keyboard.append(line)

        last_line = []

        page_btn_data = {"button_type": "change_page"}
        if start > 0:
            page_btn_data["start"] = max(0, start - self.__max_lines * self.__max_cols)
            last_line.append(InlineKeyboardButton("< Назад", callback_data=self.__pack_data(page_btn_data)))
        if count < len(names):
            page_btn_data["start"] = count + start
            last_line.append(InlineKeyboardButton("Далее >", callback_data=self.__pack_data(page_btn_data)))

        keyboard.append(last_line)
        keyboard.append(self.service_buttons)

        return InlineKeyboardMarkup(keyboard)

    def add_button(self, button: InlineKeyboardButton):
        self.service_buttons.append(button)
