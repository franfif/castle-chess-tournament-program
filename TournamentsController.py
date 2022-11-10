from Tournament import Tournament
from TournamentView import TournamentView
from TableDB import TableDB
from BaseView import BaseView
from SingleTournamentController import SingleTournamentController


class TournamentsController:
    def __init__(self, players_control):
        self.players_control = players_control
        self.view = TournamentView()
        self.base_view = BaseView()
        self.tournament_DB_Table = TableDB('tournaments')
        self.tournaments = self.get_tournaments_from_db()

    def create_tournament(self, tournament_info=None):
        tournament = SingleTournamentController(self.players_control, Tournament(*tournament_info))
        self.tournaments.append(tournament)
        self.save_tournaments_to_db()

    def save_tournaments_to_db(self):
        serialized_tournaments = []
        for tournament in self.tournaments:
            serialized_tournaments.append(tournament.serialize_tournament())
        self.tournament_DB_Table.insert_multiple(serialized_tournaments)

    def get_tournaments_from_db(self):
        serialized_tournaments = self.tournament_DB_Table.get_all_items()
        tournaments = []
        for serialized_tournament in serialized_tournaments:
            tournaments.append(SingleTournamentController(self.players_control, serialized_tournament))
        return tournaments

