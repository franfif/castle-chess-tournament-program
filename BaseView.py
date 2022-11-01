import datetime


class BaseView:
    def prompt_for_text(self, text_type):
        text = ''
        while len(text) < 1:
            text = input(f'Enter the {text_type}: ')
        return text.capitalize()

    def prompt_for_date(self, date_type):
        while True:
            try:
                date = input(f'Enter the {date_type} (mm/dd/yyyy): ')
                datetime.datetime.strptime(date, '%m/%d/%Y')
                return date
            except ValueError:
                print('Please enter a date in the format mm/dd/yyyy.')

    def prompt_for_number(self, number_type, mini=None, maxi=None):
        while True:
            try:
                number = int(input(f'Enter the {number_type}: '))
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

    def select_from_list(self, lst, proposition_zero=None, cancel_allowed=False):
        """
        Display a list of propositions and get a number from the manager
        :param lst: list of strings to display
        :param proposition_zero: string to display at the end of the propositions from list
        :param cancel_allowed: bool to allow user to cancel and stop the choice process
        :return: index of the selected item
        or -1 for the proposition_zero
        or None to cancel the selection
        """
        if proposition_zero is not None:
            print(f'[0] ** {proposition_zero} **')
        for i, e in enumerate(lst):
            print(f'[{i + 1}] {e}')
        while True:
            try:
                pick = input(f'Enter a number between {1 if proposition_zero is None else 0} '
                             f'and {len(lst)} to select a proposition or hit Return to stop: ')
                if pick == '' and cancel_allowed:
                    return None
                pick = int(pick) - 1
                if pick == -1 and proposition_zero is None:
                    continue
                elif -1 <= pick < len(lst):
                    return pick
            except ValueError:
                continue

    def order_alphabetically(self, players):
        players.sort(key=lambda x: (x.last_name, x.first_name))
        return players

    def order_by_ranking(self, players):
        players.sort(key=lambda x: x.ranking, reverse=True)
        return players

    def full_display_player(self, player):
        print(f'{player.get_full_name()}  [ '
              f'DoB: {player.date_of_birth} - '
              f'Gender: {player.gender} - '
              f'Ranking: {player.ranking} ]')

# base_view = BaseView()
# lst = ['a', 'b', 'c', 'd', 'e']
# while True:
#     print('test 1')
#     index = base_view.select_from_list(lst, 'bla')
#     if index is None:
#         break
#     elif 0 <= index <= len(lst):
#         print('==> ' + lst[index])
#     elif index == -1:
#         print('==> prop 0')
#
# while True:
#     print('test 2')
#     index = base_view.select_from_list(lst)
#     if index is None:
#         break
#     elif 0 <= index <= len(lst):
#         print('==> ' + lst[index])
#     elif index == -1:
#         print('==> prop 0')
