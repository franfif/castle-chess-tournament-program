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
    # Report Menu
    #
    def run_reports(self):
        self.generic_report_menu(self.global_report_options())

    def generic_report_menu(self, report_options):
        menu = report_options
        menu_names = list(map(lambda x: x.name, menu))
        next_action = None
        while next_action is None:
            to_do = self.base_view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        return

    def global_report_options(self):
        options = [Option('View all players', self.players_control.show_players),
                   Option('View all tournaments', self.report_tournaments),
                   Option('Exit report menu', self.exit)]
        return options

    #
    # Tournament Report Menu and Options
    #
    def report_tournaments(self):
        tournaments = self.tournaments_control.tournaments
        if len(tournaments) == 0:
            self.base_view.notice_no_tournaments_to_show()
        else:
            options = []
            for tournament in tournaments:
                options.append(Option(tournament.tournament.name, tournament.run_reports))
            options.append(Option('Back home', self.exit))
            self.generic_report_menu(options)

    @staticmethod
    def exit():
        return True
