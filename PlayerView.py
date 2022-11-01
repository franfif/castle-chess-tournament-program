from BaseView import BaseView

GENDERS = ['F', 'M', 'X', 'f', 'm', 'x']
RANKING_MIN_MAX = [1, 3000]


class PlayerView:
    def __init__(self):
        self.base_view = BaseView()

    def prompt_for_first_name(self):
        return self.base_view.prompt_for_text("player's first name")

    def prompt_for_last_name(self):
        return self.base_view.prompt_for_text("player's last name")

    def prompt_for_date_of_birth(self):
        return self.base_view.prompt_for_date("player's date of birth")

    def prompt_for_gender(self):
        gender = ''
        while gender not in GENDERS:
            gender = input("Enter the player's gender (F/M/X): ")
        return gender.capitalize()

    def prompt_for_ranking(self):
        return self.base_view.prompt_for_number("player's ranking", mini=RANKING_MIN_MAX[0], maxi=RANKING_MIN_MAX[1])

    def get_new_ranking(self, ranking, player_name):
        print(f'Until now, {player_name} had a ranking of {ranking}.')
        return self.base_view.prompt_for_number("player's new ranking", mini=RANKING_MIN_MAX[0], maxi=RANKING_MIN_MAX[1])

    def select_player(self, players):
        for i, player in enumerate(players):
            print(f'[{i + 1}] {player.get_full_name()} [ Ranking: {player.ranking} ]')
        pick = 0
        while pick < 1 or pick > len(players):
            try:
                pick = int(input(f'Enter a number between 1 and {len(players)} to select a player: '))
            except ValueError:
                continue
        return players[pick - 1]

# from Player import Player
# from TestPlayer import TestPlayer
# view = PlayerView()
# view.display_player(Player(*TestPlayer().get_data()))
