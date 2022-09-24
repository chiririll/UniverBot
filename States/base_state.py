from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes


class BaseState(ABC):

    def __init__(self, update: Update = None, context: ContextTypes.DEFAULT_TYPE = None):
        self.update = update
        self.context = context

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
