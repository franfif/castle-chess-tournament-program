from TestModel import TestPlayer, TestTournament
from PlayersController import PlayersController
from TournamentsController import TournamentsController
from BaseView import BaseView
from Option import Option
from ReportController import ReportController


class App:
    def __init__(self):
        self.players_control = PlayersController()
        self.tournaments_control = TournamentsController(self.players_control)
        self.view = BaseView()
        self.reports = ReportController(self.players_control, self.tournaments_control)

    def run(self):
        next_action = None
        while next_action is None:
            menu = self.new_app_menu()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        print('Thank you for playing! See you next time!')

    def new_app_menu(self):
        menu = [Option('Create tournament', self.create_tournament)]

        for tournament in self.tournaments_control.tournaments:
            menu.append(Option(f'Continue tournament {tournament.tournament.name}', tournament.run))

        menu.append(Option('Create players', self.create_player))

        if len(self.players_control.players) > 0:
            menu.append(Option('Edit players', self.edit_players))

        menu.append(Option('View reports', self.view_reports))

        menu.append(Option('Save and Exit', self.exit))
        return menu

    def create_player(self):
        self.players_control.create_player(TestPlayer().get_data())

    def create_tournament(self):
        self.tournaments_control.create_tournament(TestTournament().get_data())

    def edit_players(self):
        self.players_control.edit_players()

    def view_reports(self):
        self.reports.run_reports()

    def exit(self):
        self.players_control.save_players_to_db()
        self.tournaments_control.save_tournaments_to_db()
        return True


app = App()
app.run()
