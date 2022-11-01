from TestModel import TestPlayer
from TournamentView import TournamentView
from Tournament import Tournament
from PlayerController import PlayerController


class TournamentController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.view = TournamentView()
        self.all_players = self.player_controller.players
        # When tests are over, uncomment next line
        # self.tournament = self.create_tournament()
        # When tests are done, comment out next line
        self.tournament = Tournament('name', 'venue', '11/11/1111', 3, 1, 'description')

    # For the Tournament control
    def create_tournament(self):
        name = self.view.prompt_for_tournament_name()
        venue = self.view.prompt_for_venue()
        date_range = self.view.prompt_for_date_range()
        number_of_rounds = self.view.prompt_for_number_rounds()
        time_control = self.view.prompt_for_time_control()
        description = self.view.prompt_for_description()
        return Tournament(name, venue, date_range, number_of_rounds, time_control, description)

    def add_remove_tournament_players(self):
        while True:
            index = self.view.select_player(self.all_players, self.tournament.get_tournament_players())
            if index is None:
                # stop the process
                break
            elif index == -1:
                # create new player and add it to tournament players
                self.player_controller.create_player()
                self.tournament.add_player(self.all_players[index])
            elif self.all_players[index] in self.tournament.get_tournament_players():
                # remove player
                self.tournament.remove_player(self.all_players[index])
            else:
                # add player
                self.tournament.add_player(self.all_players[index])

    def start_round(self):
        pairs = self.tournament.start_new_round()
        self.view.display_pairings(pairs)

    def end_round(self):
        # end the last round created
        current_round = self.tournament.rounds[-1]
        current_round.add_end_time()
        # get winner indexes from tournament manager
        winners = self.view.prompt_for_winners(current_round)
        ended_round = []
        # attribute points to each match in the round
        for i, match in enumerate(current_round):
            ended_round.append(self.attribute_score(match, winners[i]))
        self.tournament.rounds[-1] = ended_round

    @staticmethod
    def attribute_score(match, winner):
        if winner is not None:
            match[winner][1] = 1
        else:
            match[0][1] = 0.5
            match[1][1] = 0.5
        return match

    def display_players(self):
        self.view.show_players(self.tournament.get_tournament_players())


control = PlayerController()
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())
control.create_player(TestPlayer().get_data())


# print(control.players)
test = TournamentController(control)
# test.player_controller = control
test.tournament_players = [control.players[0],
                           control.players[3],
                           control.players[6]]

test.add_remove_tournament_players()
test.display_players()
