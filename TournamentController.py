from TournamentView import TournamentView
from Tournament import Tournament
from Menu import Menu
from BaseView import BaseView


class TournamentController:
    def __init__(self, player_controller, tournament_info=None):
        self.player_controller = player_controller
        self.view = TournamentView()
        self.base_view = BaseView()
        self.all_players = self.player_controller.players
        # When tests are over, remove next 3 lines
        if tournament_info is not None:
            self.tournament = Tournament(*tournament_info)
        else:
            self.tournament = Tournament(*self.get_tournament_info())

    def get_tournament_info(self):
        name = self.view.prompt_for_tournament_name()
        venue = self.view.prompt_for_venue()
        date_range = self.view.prompt_for_date_range()
        number_of_rounds = self.view.prompt_for_number_rounds()
        time_control = self.view.prompt_for_time_control()
        description = self.view.prompt_for_description()
        return name, venue, date_range, number_of_rounds, time_control, description

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
        # get TournamentPlayers pairs from Tournament
        pairs = self.tournament.start_new_round()
        # get Players pairs from Tournament
        view_pairs = list(map(self.tournament.get_tournament_players, pairs))
        # display pairs of Players
        self.view.display_pairings(view_pairs)

    def end_round(self):
        # get the current round's pairs
        pairs = self.tournament.get_round_pairs()
        # attribute points to each match in the round
        scores = []
        for i, pair in enumerate(pairs):
            # for each pair, get the winner index from view
            winner_index = self.view.prompt_for_winner_index(pair)
            # collect scores for each pairs
            scores.append(self.attribute_score(winner_index))
        # apply scores to round to end the round
        self.tournament.end_round(scores)

    @staticmethod
    def attribute_score(winner_index):
        # default is a tie
        score = [0.5, 0.5]
        if winner_index is not None:
            # winner_index is either 0 or 1
            score[winner_index] = 1
            # 1 - winner_index is either 1 or 0, respectively
            score[1 - winner_index] = 0
        return score

    def display_players(self):
        self.view.show_players(self.tournament.get_tournament_players())

    def run(self):
        next_action = None
        while next_action is None:
            menu = self.new_menu()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.base_view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        return True

    def new_menu(self):
        menu = [Menu('Edit tournament information', self.edit_tournament_info)]

        if len(self.tournament.rounds) == 0:
            menu.append(Menu('Add/Remove tournament players', self.add_remove_tournament_players))

        if len(self.tournament.players) >= 2:
            if self.tournament.round_started:
                menu.append(Menu(f'End round', self.end_round))
            elif len(self.tournament.rounds) < self.tournament.number_of_rounds:
                menu.append(Menu('Start round', self.start_round))

        if len(self.tournament.players) > 0:
            menu.append(Menu('Show players', self.display_players))

        menu.append(Menu('Show all rounds', self.show_rounds))
        menu.append(Menu('Show all matches', self.show_matches))

        menu.append(Menu('Exit', self.exit))
        return menu

    def edit_tournament_info(self):
        # ask to change description, name, venue, etc.
        pass

    def show_rounds(self):
        # display all rounds
        self.view.display_rounds(self.tournament.rounds)

    def show_matches(self):
        print('Showing matches')

    def exit(self):
        return 'Leaving tournament'

#
# control = PlayerController()
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
# control.create_player(TestPlayer().get_data())
#
#
# # print(control.players)
# test = TournamentController(control)
# # test.player_controller = control
# test.tournament_players = [control.players[0],
#                            control.players[3],
#                            control.players[6]]
#
# test.add_remove_tournament_players()
# test.display_players()
