from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes


class BaseState(ABC):
    @abstractmethod
    def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
