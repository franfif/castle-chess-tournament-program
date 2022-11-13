from Models.MenuManager import MenuManager
from Models.Message import Message


class Option:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    @staticmethod
    def exit_option(saving=False):
        """Return an option to exit a menu with or without mentioning a saving."""
        if saving:
            return Option(Message.SAVE_AND_EXIT_MENU, MenuManager.exit)
        return Option(Message.EXIT_MENU, MenuManager.exit)
