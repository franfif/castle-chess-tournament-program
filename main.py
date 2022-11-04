from TestModel import TestPlayer, TestTournament
from PlayerController import PlayerController
from BaseView import BaseView
from TournamentController import TournamentController
from Option import Option


class App:
    def __init__(self):
        self.player_control = PlayerController()
        self.view = BaseView()
        self.tournaments = []

    def run(self):
        next_action = None
        while next_action is None:
            menu = self.new_menu()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        print('Thank you for playing! See you next time!')

    def new_menu(self):
        menu = [Option('Create tournament', self.create_tournament)]

        for tournament in self.tournaments:
            menu.append(Option(f'Continue tournament {tournament.tournament.name}', tournament.run))

        menu.append(Option('Create players', self.create_player))

        if len(self.player_control.players) > 0:
            menu.append(Option('Edit players', self.edit_players))

        menu.append(Option('View reports', self.view_reports))

        menu.append(Option('Save and Exit', self.exit))
        return menu

    def create_player(self):
        self.player_control.create_player(TestPlayer().get_data())

    def create_tournament(self):
        self.tournaments.append(TournamentController(self.player_control, TestTournament().get_data()))

    def edit_players(self):
        print('Edit players')

    def view_reports(self):
        print('view reports')

    def exit(self):
        self.player_control.save_players_to_db()
        return True


app = App()
app.run()
