from Models.MenuManager import MenuManager
from Models.Message import Message


class Option:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    @staticmethod
    def exit_option():
        return Option(Message.EXIT_MENU, MenuManager.exit)
