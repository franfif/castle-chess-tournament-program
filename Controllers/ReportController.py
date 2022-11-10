from Views.BaseView import BaseView
from Models.Option import Option


class ReportController:
    def __init__(self, players_control, tournaments_control):
        self.players_control = players_control
        self.tournaments_control = tournaments_control
        self.base_view = BaseView()

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

    def report_tournaments(self):
        tournaments = self.tournaments_control.tournaments
        if len(tournaments) == 0:
            # self.view.notice_no_tournaments_to_show()
            pass
        else:
            options = []
            for tournament in tournaments:
                options.append(Option(tournament.tournament.name, tournament.run_reports))
            options.append(Option('Back home', self.exit))
            self.generic_report_menu(options)

    def exit(self):
        return True
