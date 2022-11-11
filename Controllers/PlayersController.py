from Views.PlayerView import PlayerView
from DB.TableDB import TableDB
from Views.BaseView import BaseView
from Controllers.SinglePlayerController import SinglePlayerController
from Models.Option import Option
from Models.Message import Message
from Models.MenuManager import MenuManager


class PlayersController:
    def __init__(self):
        self.view = PlayerView()
        self.base_view = BaseView()
        self.player_DB_Table = TableDB('players')
        self.players = self.get_players_from_db()

    def create_player(self):
        self.players.append(SinglePlayerController())
        self.save_players_to_db()

    def edit_players(self, players=None):
        next_action = None
        while next_action is None:
            if players is None:
                players = self.players
            player_info = list(map(lambda x: self.view.get_full_info_player(x.player), players))
            pick = self.base_view.select_from_list(player_info, cancel_allowed=True)
            if pick is None:
                break
            players[pick].edit_player_menu()
            self.save_players_to_db()
        return

    #
    # Display Methods
    #
    def show_players(self, players=None):
        """
        Get a list of players and fetch the order preference from the view.
        Call view to show the players in the given order
        :param players: a list of SinglePlayerControllers
        :return : Nothing
        """
        if players is None:
            players = list(map(lambda x: x.player, self.players))
        if len(players) == 0:
            self.view.notice_no_players_to_show()
        else:
            if self.view.prompt_for_order_preference(['Ranking', 'Alphabetical']) == 0:
                players = self.order_by_ranking(players)
            else:
                players = self.order_alphabetically(players)
            self.view.show_players(players)

    @staticmethod
    def order_by_ranking(players):
        players.sort(key=lambda x: x.ranking, reverse=True)
        return players

    @staticmethod
    def order_alphabetically(players):
        players.sort(key=lambda x: (x.last_name, x.first_name))
        return players

    #
    # Database Linking Method
    #
    def save_players_to_db(self):
        """
        Fetch serialized players and send them to the tableDB manager
        """
        serialized_players = []
        for player in self.players:
            serialized_players.append(player.serialize_player())
        self.player_DB_Table.insert_multiple(serialized_players)

    def get_players_from_db(self):
        """
        Fetch serialized players from TinyDB file and create SinglePlayerControllers
        :return: list of SinglePlayerControllers
        """
        serialized_players = self.player_DB_Table.get_all_items()
        players = []
        for serialized_player in serialized_players:
            players.append(SinglePlayerController(serialized_player))
        return players
