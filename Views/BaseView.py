import datetime
import os
from Models.Message import Message


class BaseView:

    #
    # Input Methods
    #
    @staticmethod
    def prompt_for_text(text_type):
        text = ''
        while len(text) < 1:
            text = input(f'Enter the {text_type}: ')
        return text

    @staticmethod
    def prompt_for_date(date_type):
        while True:
            try:
                date = input(f'Enter the {date_type} (mm/dd/yyyy): ')
                datetime.datetime.strptime(date, '%m/%d/%Y')
                return date
            except ValueError:
                print('Please enter a date in the format mm/dd/yyyy.')

    @staticmethod
    def prompt_for_number(number_type, mini=None, maxi=None, default=None):
        instructions = f'Enter the {number_type}'
        instructions += f' (default = {default}): ' if default else ': '
        while True:
            try:
                number = input(instructions)
                if number == '' and default is not None:
                    return default
                number = int(number)
                if (maxi is None or number <= maxi) and (mini is None or mini <= number):
                    return number
                else:
                    raise ValueError
            except ValueError:
                if maxi is None:
                    if mini is None:
                        print('Please enter a number')
                    else:
                        print(f'Please enter a number superior or equal to {mini}.')
                else:
                    if mini is None:
                        print(f'Please enter a number inferior or equal to {maxi}.')
                    else:
                        print(f'Please enter a number between {mini} and {maxi}.')

    #
    # Choice Input Method
    #
    @staticmethod
    def select_from_list(lst, option_zero=None, cancel_allowed=False):
        """
        Display a list of options and get a number from the manager
        :param lst: list of strings to display
        :param option_zero: string to display at the top of the options
        :param cancel_allowed: boolean to allow user to cancel and stop the selection process
        :return: index of the selected item or -1 for option_zero or None to cancel the selection
        """
        if option_zero is not None:
            print(f'[0] ** {option_zero} **')
        if len(lst) == 1 and option_zero is None:
            input(f'Press Enter to {lst[0]}')
            return 0
        for i, e in enumerate(lst):
            print(f'[{i + 1}] {e}')
        while True:
            try:
                pick = input(f'Enter a number between {1 if option_zero is None else 0} '
                             f'and {len(lst)} to select an option'
                             f'{" or press Enter to stop: " if cancel_allowed else ": "}')
                if pick == '' and cancel_allowed:
                    return None
                pick = int(pick) - 1
                if pick == -1 and option_zero is None:
                    continue
                elif -1 <= pick < len(lst):
                    return pick
            except ValueError:
                continue

    #
    # Display Method
    #
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def welcome_message():
        BaseView.display_titles((Message.PROGRAM_NAME, Message.LOGO_ASCII, Message.WELCOME))
        input(Message.START_PROGRAM)

    @staticmethod
    def good_bye_message():
        BaseView.display_titles((Message.PROGRAM_NAME, Message.LOGO_ASCII, Message.GOOD_BYE))

    @staticmethod
    def display_titles(titles):
        BaseView.clear_screen()
        line_length = 64

        def print_line(header):
            half = line_length // 2 - len(header) // 2
            print(' ' * half + header)

        print('~' * line_length)
        if isinstance(titles, str):
            print_line(titles)
        elif isinstance(titles, tuple):
            for title in titles:
                if isinstance(title, str):
                    print_line(title)
        print('~' * line_length)
