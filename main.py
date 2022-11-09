from TestModel import TestPlayer, TestTournament
from PlayerController import PlayerController
from BaseView import BaseView
from TournamentController import TournamentController
from Option import Option
from TableDB import TableDB


class App:
    def __init__(self):
        self.player_control = PlayerController()
        self.view = BaseView()
        self.tournament_DB_Table = TableDB('tournaments')
        self.tournaments = self.get_tournaments_from_db()

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
        self.save_tournaments_to_db()

    def edit_players(self):
        self.player_control.edit_players()

    def view_reports(self):
        print('view reports')

    def exit(self):
        self.player_control.save_players_to_db()
        self.save_tournaments_to_db()
        return True

    def save_tournaments_to_db(self):
        serialized_tournaments = []
        for tournament in self.tournaments:
            serialized_tournaments.append(tournament.serialize_tournament())
        self.tournament_DB_Table.insert_multiple(serialized_tournaments)

    def get_tournaments_from_db(self):
        serialized_tournaments = self.tournament_DB_Table.get_all_items()
        tournaments = []
        for serialized_tournament in serialized_tournaments:
            tournaments.append(TournamentController(self.player_control, serialized_tournament))
        return tournaments


app = App()
app.run()
