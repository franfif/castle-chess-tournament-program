# from Tests.TestModel import TestPlayer, TestTournament
from Controllers.PlayersController import PlayersController
from Controllers.TournamentsController import TournamentsController
from Views.BaseView import BaseView
from Models.Option import Option
from Controllers.ReportController import ReportController


class App:
    def __init__(self):
        self.players_control = PlayersController()
        self.tournaments_control = TournamentsController(self.players_control)
        self.view = BaseView()
        self.reports = ReportController(self.players_control, self.tournaments_control)

    def run(self):
        self.generic_app_menu(self.app_options)
        print('Thank you for playing! See you next time!')

    def generic_app_menu(self, get_menu_options):
        next_action = None
        while next_action is None:
            menu = get_menu_options()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        return

    def app_options(self):
        menu = [Option('Create tournament', self.create_tournament)]

        ongoing_tournaments = list(filter(lambda x: not x.tournament.has_ended(),
                                          self.tournaments_control.tournaments))
        for tournament in ongoing_tournaments:
            menu.append(Option(f'Continue tournament {tournament.tournament.name}', tournament.run))

        menu.append(Option('Create players', self.create_player))

        if len(self.players_control.players) > 0:
            menu.append(Option('Edit players', self.edit_players))

        menu.append(Option('View reports', self.view_reports))

        archived_tournaments = list(filter(lambda x: x.tournament.has_ended(),
                                           self.tournaments_control.tournaments))
        if len(archived_tournaments) > 0:
            menu.append(Option('Archived tournaments', self.edit_archived_tournaments))

        menu.append(Option('Save and Exit', self.exit))
        return menu

    def create_player(self):
        self.players_control.create_player()

    def create_tournament(self):
        self.tournaments_control.create_tournament()

    def edit_players(self):
        self.players_control.edit_players()

    def view_reports(self):
        self.reports.run_reports()

    def edit_archived_tournaments(self):
        self.generic_app_menu(self.archived_tournaments_options)

    def archived_tournaments_options(self):
        archived_tournaments = list(filter(lambda x: x.tournament.has_ended(),
                                           self.tournaments_control.tournaments))
        options = []
        for tournament in archived_tournaments:
            options.append(Option(f'Tournament {tournament.tournament.name}', tournament.run))
        options.append(Option('Back', self.exit))
        return options

    def exit(self):
        self.players_control.save_players_to_db()
        self.tournaments_control.save_tournaments_to_db()
        return True


app = App()
app.run()
