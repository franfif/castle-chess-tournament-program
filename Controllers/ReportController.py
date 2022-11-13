from Views.BaseView import BaseView
from Models.Option import Option
from Models.MenuManager import MenuManager
from Models.Message import Message


class ReportController:
    def __init__(self, players_control, tournaments_control):
        self.players_control = players_control
        self.tournaments_control = tournaments_control
        self.base_view = BaseView()

    #
    # Report Main Menu and Options
    #
    def run_reports(self):
        MenuManager.menu(get_options_method=self.main_report_options,
                         titles=Message.REPORT_MENU)

    def main_report_options(self):
        options = [Option('View all players', self.players_control.run_all_players_report),
                   Option('View all tournaments', self.run_tournament_reports),
                   Option.exit_option()]
        return options

    #
    # Tournament Report Menu and Options
    #
    def run_tournament_reports(self):
        MenuManager.menu(get_options_method=self.tournament_report_options,
                         titles=(Message.REPORT_MENU, Message.TOURNAMENTS_TITLE))

    def tournament_report_options(self):
        tournaments = self.tournaments_control.tournaments
        if len(tournaments) == 0:
            return [Option(Message.NO_TOURNAMENTS, MenuManager.exit)]
        options = []
        for tournament in tournaments:
            options.append(Option(tournament.tournament.name, tournament.run_reports))
        options.append(Option.exit_option())
        return options
