from Views.PlayerView import PlayerView
from DB.TableDB import TableDB
from Controllers.SinglePlayerController import SinglePlayerController
from Models.Option import Option
from Models.Message import Message
from Controllers.MenuManager import MenuManager


class PlayersController:
    def __init__(self):
        self.view = PlayerView()
        self.player_DB_Table = TableDB('players')
        self.players = self.get_players_from_db()

    def create_player(self):
        # Display a title
        self.view.display_titles(Message.CREATE_PLAYER_MENU)
        # Initialize a new player
        new_player = SinglePlayerController()
        self.players.append(new_player)
        # Update the players database table
        self.save_players_to_db()

    #
    # Edit Players Menu and Options
    #
    def edit_players(self):
        """Send players to MenuManager to allow user to edit them."""
        MenuManager.menu(get_options_method=self.edit_players_options,
                         titles=Message.EDIT_PLAYERS_MENU,
                         save_method=self.save_players_to_db)

    def edit_players_options(self, players=None):
        if players is None:
            players = self.players

        options = []
        for player in players:
            options.append(Option(self.view.get_full_info_player(player.player), player.edit_player_menu))
        options.append(Option.exit_option(saving=True))
        return options

    #
    # Report Menu and Options
    #
    def run_all_players_report(self):
        """Send all players information for the MenuManager to display."""
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
        """Fetch the players order preference from the view and return the sorted list of players."""
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
        """Serialize all players and send them to players DB table."""
        serialized_players = []
        for player in self.players:
            serialized_players.append(player.serialize_player())
        self.player_DB_Table.insert_multiple(serialized_players)

    def get_players_from_db(self):
        """Fetch serialized players from TinyDB file and return a list of SinglePlayerController objects."""
        serialized_players = self.player_DB_Table.get_all_items()
        players = []
        for serialized_player in serialized_players:
            players.append(SinglePlayerController(serialized_player))
        return players
