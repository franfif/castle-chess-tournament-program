from Controllers.PlayersController import PlayersController
from Controllers.TournamentsController import TournamentsController
from Views.BaseView import BaseView
from Models.Option import Option
from Controllers.ReportController import ReportController
from Models.Message import Message
from Controllers.MenuManager import MenuManager


class App:
    def __init__(self):
        self.players_control = PlayersController()
        self.tournaments_control = TournamentsController(self.players_control)
        self.view = BaseView()
        self.reports_control = ReportController(self.players_control, self.tournaments_control)

    def run(self):
        self.view.welcome_message()
        MenuManager.menu(get_options_method=self.app_options,
                         titles=Message.MAIN_MENU)
        self.view.good_bye_message()

    def app_options(self):
        menu = [Option('New tournament', self.create_tournament)]

        ongoing_tournaments = list(filter(lambda x: not x.tournament.has_ended(),
                                          self.tournaments_control.tournaments))
        for tournament_control in ongoing_tournaments:
            menu.append(Option(f'Open [ {tournament_control.tournament.name} ]', tournament_control.run))

        menu.append(Option('New player', self.create_player))

        if len(self.players_control.players) > 0:
            menu.append(Option('Edit players', self.edit_players))

        if len(self.tournaments_control.tournaments) > 0 or len(self.players_control.players) > 0:
            menu.append(Option('Reports', self.view_reports))

        archived_tournaments = list(filter(lambda x: x.tournament.has_ended(),
                                           self.tournaments_control.tournaments))
        if len(archived_tournaments) > 0:
            menu.append(Option('Archived tournaments', self.edit_archived_tournaments))

        menu.append(Option(Message.LEAVE_APP_MENU, MenuManager.exit))
        return menu

    def create_player(self):
        self.players_control.create_player()

    def create_tournament(self):
        tournament = self.tournaments_control.create_tournament()
        tournament.run()

    def edit_players(self):
        self.players_control.edit_players()

    def view_reports(self):
        self.reports_control.run_reports()

    def edit_archived_tournaments(self):
        MenuManager.menu(get_options_method=self.archived_tournaments_options,
                         titles=Message.ARCHIVED_TOURNAMENT_MENU)

    def archived_tournaments_options(self):
        archived_tournaments = list(filter(lambda x: x.tournament.has_ended(),
                                           self.tournaments_control.tournaments))
        options = []
        for tournament in archived_tournaments:
            options.append(Option(f'Tournament {tournament.tournament.name}', tournament.run))
        options.append(Option.exit_option())
        return options


app = App()
app.run()
