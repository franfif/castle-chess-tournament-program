from Player import Player
from PlayerView import PlayerView
from TableDB import TableDB
from BaseView import BaseView
from Option import Option


class PlayerController:
    def __init__(self):
        self.view = PlayerView()
        self.base_view = BaseView
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

    def display_players(self, players=None):
        if players is None:
            players = self.players
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
        next_action = None
        while next_action is None:
            player = self.view.select_player_full_info(players)
            while next_action is None:
                menu = self.edit_player_options()
                menu_names = list(map(lambda x: x.name, menu))
                to_do = self.base_view.select_from_list(menu_names)
                next_action = menu[to_do].function(player)
        return

    def edit_player_options(self):
        options = [Option('Change first name', self.update_first_name),
                   Option('Change last name', self.update_last_name),
                   Option('Change date of birth', self.update_date_of_birth),
                   Option('Change gender', self.update_gender),
                   Option('Change ranking', self.update_ranking),
                   Option('Back to all players', self.exit)]
        return options

    def update_first_name(self, player):
        new_first_name = self.view.get_new_ranking(player.ranking, player.get_full_name())
        player.ranking = new_ranking
        self.save_players_to_db()

    def update_last_name(self, player):
        new_ranking = self.view.get_new_ranking(player.ranking, player.get_full_name())
        player.ranking = new_ranking
        self.save_players_to_db()

    def update_date_of_birth(self, player):
        new_ranking = self.view.get_new_ranking(player.ranking, player.get_full_name())
        player.ranking = new_ranking
        self.save_players_to_db()

    def update_gender(self, player):
        new_ranking = self.view.get_new_ranking(player.ranking, player.get_full_name())
        player.ranking = new_ranking
        self.save_players_to_db()

    def update_ranking(self, player):
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
