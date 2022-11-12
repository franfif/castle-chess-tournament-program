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

    #
    # Edit Players Menu and Options
    #
    def edit_players(self):
        MenuManager.menu(get_options_method=self.edit_players_options,
                         titles=Message.EDIT_PLAYERS_MENU,
                         save_method=self.save_players_to_db)

    def edit_players_options(self, players=None):
        if players is None:
            players = self.players

        options = []
        for player in players:
            options.append(Option(self.view.get_full_info_player(player.player), player.edit_player_menu))
        options.append(Option(Message.EXIT_MENU, MenuManager.exit))
        return options

    #
    # Report Menu and Options
    #
    def run_all_player_reports(self):
        players = self.get_players_in_preferred_order()
        MenuManager.menu(get_options_method=self.exit_only_option,
                         titles=(Message.REPORT_MENU, Message.PLAYERS_TITLE),
                         content=(self.view.display_players, players))

    @staticmethod
    def exit_only_option():
        return [Option.exit_option()]

    #
    # Sorting Methods
    #
    def get_players_in_preferred_order(self, players=None):
        """
        Get a list of players and fetch the order preference from the view.
        Call view to show the players in the given order
        :param players: a list of SinglePlayerControllers
        :return : Nothing
        """
        if players is None:
            players = list(map(lambda x: x.player, self.players))
        if self.view.prompt_for_order_preference([Message.RANKING, Message.ALPHABETICAL]) == 0:
            players = self.sort_by_ranking(players)
        else:
            players = self.sort_alphabetically(players)
        return players

    def sort_by_ranking(self, players=None):
        if players is None:
            players = list(map(lambda x: x.player, self.players))
        players.sort(key=lambda x: x.ranking, reverse=True)
        return players

    def sort_alphabetically(self, players=None):
        if players is None:
            players = list(map(lambda x: x.player, self.players))
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
