from Player import Player
from PlayerView import PlayerView


class PlayerController:
    def __init__(self):
        self.view = PlayerView()
        self.players = []

    def get_player_info(self):
        first_name = self.view.prompt_for_first_name()
        last_name = self.view.prompt_for_last_name()
        date_of_birth = self.view.prompt_for_date_of_birth()
        gender = self.view.prompt_for_gender()
        ranking = self.view.prompt_for_ranking()
        return first_name, last_name, date_of_birth, gender, ranking

    def create_player(self, player_info=None):
        if player_info is None:
            player_info = self.get_player_info()
        player = Player(*player_info)
        self.players.append(player)

    def change_ranking(self):
        player = self.view.select_player_ranking(self.players)
        new_ranking = self.view.get_new_ranking(player.ranking, player.get_full_name())
        player.ranking = new_ranking
