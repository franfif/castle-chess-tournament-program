# from Tournament import Tournament
# from Player import Player
from TestModel import TestPlayer, TestTournament
# from PlayerView import PlayerView
from PlayerController import PlayerController
from BaseView import BaseView
from TournamentController import TournamentController
from Menu import Menu


MENU_INITIAL = ['Create tournament',
                'Add players',
                'Edit players',
                'View reports']


class App:
    def __init__(self):
        self.player_control = PlayerController()
        self.view = BaseView()
        self.tournament = None

    def run(self):
        next_action = None
        while next_action is None:
            menu = self.new_menu()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        print(next_action)

    def new_menu(self):
        menu = []
        if self.tournament is None:
            menu.append(Menu('Create tournament', self.create_tournament))
        else:
            menu.append(Menu(f'Continue tournament {self.tournament.tournament.name}', self.continue_tournament))

        menu.append(Menu('Create players', self.create_player))

        if len(self.player_control.players) > 0:
            menu.append(Menu('Edit players', self.edit_players))

        menu.append(Menu('View reports', self.view_reports))

        menu.append(Menu('Exit', self.exit))
        return menu

    def create_player(self):
        self.player_control.create_player(TestPlayer().get_data())

    def create_tournament(self):
        self.tournament = TournamentController(self.player_control, TestTournament().get_data())

    def continue_tournament(self):
        self.tournament.run()

    def edit_players(self):
        print('Edit players')

    def view_reports(self):
        print('view reports')

    @staticmethod
    def exit():
        return 'Thank you for playing! See you next time!'


app = App()
# print(TestTournament().get_data())
# app.tournament = (TournamentController(app.player_control, TestTournament().get_data()))
app.run()

# tournament_control = TournamentController(player_control)
# tournament_control.add_remove_tournament_players()


#
# tournament = Tournament('test', 'here', 'now', 4, 'blitz',
#                         'This is a description')
#
# test_player1 = TestPlayer()
# test_player2 = TestPlayer()
# test_player3 = TestPlayer()
# test_player4 = TestPlayer()
# test_player5 = TestPlayer()
# test_player6 = TestPlayer()
# test_player7 = TestPlayer()
# test_player8 = TestPlayer()
#
# tournament.add_player(Player(*test_player1.get_data()))
# tournament.add_player(Player(*test_player2.get_data()))
# tournament.add_player(Player(*test_player3.get_data()))
# tournament.add_player(Player(*test_player4.get_data()))
# tournament.add_player(Player(*test_player5.get_data()))
# tournament.add_player(Player(*test_player6.get_data()))
# tournament.add_player(Player(*test_player7.get_data()))
# tournament.add_player(Player(*test_player8.get_data()))
#
#
# # for player1, player2 in tournament.sort_players_by_ranking():
# #     print(player1.ranking, player2.ranking)
#
# view = PlayerView()
# control = PlayerController()
# control.create_player(test_player1.get_data())
# control.create_player(test_player2.get_data())
# control.create_player(test_player3.get_data())
# control.create_player(test_player4.get_data())
# control.create_player(test_player5.get_data())
# control.create_player(test_player6.get_data())
# control.create_player(test_player7.get_data())
# control.create_player(test_player8.get_data())
#
# control.change_ranking()
#

