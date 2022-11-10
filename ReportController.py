from BaseView import BaseView
from Option import Option


class ReportController:
    def __init__(self, players_control, tournaments_control):
        self.players_control = players_control
        self.tournaments = tournaments_control.tournaments
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
        options = [Option('View all players', self.players_control.display_players),
                   Option('View all tournaments', self.report_tournaments),
                   Option('Exit report menu', self.exit)]
        return options

    # def report_players(self, players):
    #     if players is None:
    #         players = self.players_control.players
    #     if len(players) == 0:
    #         self.view.notice_no_players_to_show()
    #     else:
    #         if self.view.prompt_for_order_preference(['ranking', 'alphabetical']) == 0:
    #             players = play.order_by_ranking(players)
    #         else:
    #             players = self.order_alphabetically(players)
    #         # either:
    #         self.view.show_players(players)
    #         # or, if players is a list of SinglePlayerControllers:
    #         for player in players:
    #             player.display_player()
    #
    # def order_by_ranking(self, players):
    #     players.sort(key=lambda x: x.ranking, reverse=True)
    #     return players
    #
    # def order_alphabetically(self, players):
    #     players.sort(key=lambda x: (x.last_name, x.first_name))
    #     return players

    def report_tournaments(self, tournaments=None):
        if tournaments is None:
            tournaments = self.tournaments
        if len(tournaments) == 0:
            # self.view.notice_no_tournaments_to_show()
            pass
        else:
            options = []
            for tournament in tournaments:
                options.append(Option(tournament.name, ))

    def exit(self):
        pass

