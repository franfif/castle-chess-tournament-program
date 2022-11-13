from Views.PlayerView import PlayerView
from Views.BaseView import BaseView
from Models.Player import Player
from Models.Option import Option
from Models.Message import Message
from Models.MenuManager import MenuManager


class SinglePlayerController:
    def __init__(self, player=None):
        self.view = PlayerView()
        self.base_view = BaseView()
        if player is not None:
            self.player = self.deserialize_player(player)
        else:
            self.player = Player(*self.get_player_info())

    def get_player_info(self):
        first_name = self.view.prompt_for_first_name()
        last_name = self.view.prompt_for_last_name()
        date_of_birth = self.view.prompt_for_date_of_birth()
        gender = self.view.prompt_for_gender()
        ranking = self.view.prompt_for_ranking()
        return first_name, last_name, date_of_birth, gender, ranking

    #
    # Edit Player Menu
    #
    def edit_player_menu(self):
        MenuManager.menu(get_options_method=self.edit_player_options,
                         titles=Message.EDIT_PLAYERS_MENU,
                         content=(self.view.display_players, self.player))

    def edit_player_options(self):
        options = [Option(Message.UPDATE_FIRST_NAME, self.update_first_name),
                   Option(Message.UPDATE_LAST_NAME, self.update_last_name),
                   Option(Message.UPDATE_DATE_OF_BIRTH, self.update_date_of_birth),
                   Option(Message.UPDATE_GENDER, self.update_gender),
                   Option(Message.UPDATE_RANKING, self.update_ranking),
                   Option.exit_option()]
        return options

    #
    # Edit Player Methods
    #
    def update_first_name(self):
        new_first_name = self.view.get_new_first_name(self.player.get_full_name())
        self.player.first_name = new_first_name

    def update_last_name(self):
        new_last_name = self.view.get_new_last_name(self.player.get_full_name())
        self.player.last_name = new_last_name

    def update_date_of_birth(self):
        new_date_of_birth = self.view.get_new_date_of_birth(self.player.get_full_name(), self.player.date_of_birth)
        self.player.date_of_birth = new_date_of_birth

    def update_gender(self):
        new_gender = self.view.get_new_gender(self.player.get_full_name(), self.player.gender)
        self.player.gender = new_gender

    def update_ranking(self):
        new_ranking = self.view.get_new_ranking(self.player.ranking, self.player.get_full_name())
        self.player.ranking = new_ranking

    #
    # Serialization - Deserialization Methods
    #
    def serialize_player(self):
        serialized_player = {
            'first_name': self.player.first_name,
            'last_name': self.player.last_name,
            'date_of_birth': self.player.date_of_birth,
            'gender': self.player.gender,
            'ranking': self.player.ranking,
            'id': self.player.id
        }
        return serialized_player

    @staticmethod
    def deserialize_player(serialized_player):
        player = Player(first_name=serialized_player['first_name'],
                        last_name=serialized_player['last_name'],
                        date_of_birth=serialized_player['date_of_birth'],
                        gender=serialized_player['gender'],
                        ranking=serialized_player['ranking'],
                        player_id=serialized_player['id'])
        return player
