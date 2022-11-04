from Player import Player
from PlayerView import PlayerView
from TableDB import TableDB


class PlayerController:
    def __init__(self):
        self.view = PlayerView()
        self.player_DB_Table = TableDB('players')
        self.players = self.get_players_from_db()

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
        self.save_players_to_db()

    def change_ranking(self):
        player = self.view.select_player_ranking(self.players)
        new_ranking = self.view.get_new_ranking(player.ranking, player.get_full_name())
        player.ranking = new_ranking
        self.save_players_to_db()

    def save_players_to_db(self):
        serialized_players = []
        for player in self.players:
            serialized_player = {
                'first_name': player.first_name,
                'last_name': player.last_name,
                'date_of_birth': player.date_of_birth,
                'gender': player.gender,
                'ranking': player.ranking,
            }
            serialized_players.append(serialized_player)
        self.player_DB_Table.insert_multiple(serialized_players)

    def get_players_from_db(self):
        serialized_players = self.player_DB_Table.get_all_items()
        players = []
        for serialized_player in serialized_players:
            player = Player(
                first_name=serialized_player['first_name'],
                last_name=serialized_player['last_name'],
                date_of_birth=serialized_player['date_of_birth'],
                gender=serialized_player['gender'],
                ranking=serialized_player['ranking']
            )
            players.append(player)
        return players
