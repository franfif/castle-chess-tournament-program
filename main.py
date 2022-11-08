from TestModel import TestPlayer, TestTournament
from PlayerController import PlayerController
from BaseView import BaseView
from TournamentController import TournamentController
from Option import Option
from TableDB import TableDB
from Round import Round


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
            rounds = []
            for rnd in serialized_tournament['rounds']:
                matches = []
                for [[player1_id, score1], [player2_id, score2]] in rnd['matches']:
                    player1 = list(filter(lambda x: x.player.id == player1_id, self.player_control.players))
                    player1 = player1[0].player
                    player2 = list(filter(lambda x: x.player.id == player2_id, self.player_control.players))
                    player2 = player2[0].player
                    matches.append(([player1, score1], [player2, score2]))
                rounds.append(Round(name=rnd['name'],
                                    matches=matches,
                                    start_time=rnd['start_time'],
                                    end_time=rnd['end_time']
                                    ))
            tournament = TournamentController(
                self.player_control,
                (
                    serialized_tournament['name'],
                    serialized_tournament['venue'],
                    serialized_tournament['date'],
                    serialized_tournament['number_of_rounds'],
                    serialized_tournament['time_control'],
                    serialized_tournament['description'],
                    rounds,
                    [x.player for x in self.player_control.players if x.player.id in serialized_tournament['players']],
                    serialized_tournament['round_started']
                )
            )
            tournaments.append(tournament)
        return tournaments


app = App()
app.run()
