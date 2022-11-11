from Views.TournamentView import TournamentView
from DB.TableDB import TableDB
from Views.BaseView import BaseView
from Controllers.SingleTournamentController import SingleTournamentController


class TournamentsController:
    def __init__(self, players_control):
        self.players_control = players_control
        self.view = TournamentView()
        self.base_view = BaseView()
        self.tournament_DB_Table = TableDB('tournaments')
        self.tournaments = self.get_tournaments_from_db()

    def create_tournament(self):
        """
        Create a new tournament and send it in return to run it directly if needed
        :return: tournament
        """
        tournament = SingleTournamentController(self.players_control, self)
        self.tournaments.append(tournament)
        self.save_tournaments_to_db()
        return tournament

    #
    # Database Linking Method
    #
    def save_tournaments_to_db(self):
        serialized_tournaments = []
        for tournament in self.tournaments:
            serialized_tournaments.append(tournament.serialize_tournament())
        self.tournament_DB_Table.insert_multiple(serialized_tournaments)

    def get_tournaments_from_db(self):
        serialized_tournaments = self.tournament_DB_Table.get_all_items()
        tournaments = []
        for serialized_tournament in serialized_tournaments:
            tournaments.append(SingleTournamentController(self.players_control, self, serialized_tournament))
        return tournaments
