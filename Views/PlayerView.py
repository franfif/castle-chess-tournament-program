from Views.BaseView import BaseView
from Models.Message import Message


GENDERS = ['F', 'M', 'X', 'f', 'm', 'x']
RANKING_MIN_MAX = [1, 3000]


class PlayerView:
    def __init__(self):
        self.base_view = BaseView()

    #
    # Original Input Methods
    #
    def prompt_for_first_name(self):
        return self.base_view.prompt_for_text("player's first name")

    def prompt_for_last_name(self):
        return self.base_view.prompt_for_text("player's last name")

    def prompt_for_date_of_birth(self):
        return self.base_view.prompt_for_date("player's date of birth")

    @staticmethod
    def prompt_for_gender():
        gender = ''
        while gender not in GENDERS:
            gender = input("Enter the player's gender (F/M/X): ")
        return gender.capitalize()

    def prompt_for_ranking(self):
        return self.base_view.prompt_for_number("player's ranking", mini=RANKING_MIN_MAX[0], maxi=RANKING_MIN_MAX[1])

    #
    # Update Input Methods
    #
    def get_new_first_name(self, player_name):
        return self.base_view.prompt_for_text(f"{player_name}'s new first name")

    def get_new_last_name(self, player_name):
        return self.base_view.prompt_for_text(f"{player_name}'s new last name")

    def get_new_date_of_birth(self, player_name, date_of_birth):
        print(f"{player_name}'s current date of birth: {date_of_birth}.")
        return self.base_view.prompt_for_date("player's new date of birth")

    def get_new_gender(self, player_name, gender):
        print(f"{player_name}'s current gender: {gender}.")
        return self.prompt_for_gender()

    def get_new_ranking(self, ranking, player_name):
        print(f"{player_name}'s current ranking: {ranking}.")
        return self.base_view.prompt_for_number(f"{player_name}'s new ranking",
                                                mini=RANKING_MIN_MAX[0],
                                                maxi=RANKING_MIN_MAX[1])

    #
    # Choice Input Method
    #
    def prompt_for_order_preference(self, choices):
        print('How would you like to order the players?')
        return self.base_view.select_from_list(choices)

    #
    # Display Methods
    #
    def show_players(self, players):
        for player in players:
            print(self.get_full_info_player(player))

    @staticmethod
    def get_full_info_player(player):
        return (f'{player.get_full_name()}  [ '
                f'DoB: {player.date_of_birth} - '
                f'Gender: {player.gender} - '
                f'Ranking: {player.ranking} ]')

    #
    # Notice Method
    #
    @staticmethod
    def notice_no_players_to_show():
        print('No players to show.')
