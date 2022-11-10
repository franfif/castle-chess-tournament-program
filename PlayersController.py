from Player import Player
from PlayerView import PlayerView
from TableDB import TableDB
from BaseView import BaseView
from SinglePlayerController import SinglePlayerController


class PlayersController:
    def __init__(self):
        self.view = PlayerView()
        self.base_view = BaseView()
        self.player_DB_Table = TableDB('players')
        self.players = self.get_players_from_db()

    def create_player(self, player_info=None):
        player = SinglePlayerController(Player(*player_info))
        self.players.append(player)
        self.save_players_to_db()

    def display_players(self, players=None):
        if players is None:
            players = list(map(lambda x: x.player, self.players))
        if len(players) == 0:
            self.view.notice_no_players_to_show()
        else:
            if self.view.prompt_for_order_preference(['ranking', 'alphabetical']) == 0:
                players = self.order_by_ranking(players)
            else:
                players = self.order_alphabetically(players)
            self.view.show_players(players)

    def order_by_ranking(self, players):
        players.sort(key=lambda x: x.ranking, reverse=True)
        return players

    def order_alphabetically(self, players):
        players.sort(key=lambda x: (x.last_name, x.first_name))
        return players

    def edit_players(self, players=None):
        if players is None:
            players = self.players
        player_names = list(map(lambda x: self.view.full_info_player(x.player), players))

        next_action = None
        while next_action is None:
            pick = self.base_view.select_from_list(player_names, cancel_allowed=True)
            if pick is None:
                break
            players[pick].edit_player()
            self.save_players_to_db()
        return

    def save_players_to_db(self):
        serialized_players = []
        for player in self.players:
            serialized_player = {
                'first_name': player.player.first_name,
                'last_name': player.player.last_name,
                'date_of_birth': player.player.date_of_birth,
                'gender': player.player.gender,
                'ranking': player.player.ranking,
                'id': player.player.id
            }
            serialized_players.append(serialized_player)
        self.player_DB_Table.insert_multiple(serialized_players)

    def get_players_from_db(self):
        serialized_players = self.player_DB_Table.get_all_items()
        players = []
        for serialized_player in serialized_players:
            player = SinglePlayerController(Player(first_name=serialized_player['first_name'],
                                                   last_name=serialized_player['last_name'],
                                                   date_of_birth=serialized_player['date_of_birth'],
                                                   gender=serialized_player['gender'],
                                                   ranking=serialized_player['ranking'],
                                                   player_id=serialized_player['id']))
            players.append(player)
        return players
