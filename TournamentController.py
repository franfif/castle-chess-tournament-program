from TournamentView import TournamentView
from Tournament import Tournament
from Option import Option
from BaseView import BaseView


class TournamentController:
    def __init__(self, player_controller, tournament_info=None):
        self.player_controller = player_controller
        self.view = TournamentView()
        self.base_view = BaseView()
        self.all_players = list(map(lambda x: x.player, self.player_controller.players))
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
        pairs = self.tournament.start_new_round()
        if pairs:
            self.view.display_pairings(pairs)
        else:
            self.view.notice_no_more_pairings()
            self.end_tournament()

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

    def end_tournament(self):
        self.tournament.number_of_rounds = len(self.tournament.rounds)
        self.view.notice_tournament_over()

    @staticmethod
    def attribute_score(winner_index):
        score = [0.5, 0.5]
        if winner_index is not None:
            score[winner_index] = 1
            score[1 - winner_index] = 0
        return score

    def display_players(self):
        self.player_controller.display_players(self.tournament.get_tournament_players())

    def run(self):
        next_action = None
        while next_action is None:
            self.base_view.display_title('Tournament ' + self.tournament.name)
            menu = self.new_menu()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.base_view.select_from_list(menu_names)
            next_action = menu[to_do].function()
        return

    def new_menu(self):
        menu = [Option('Edit tournament information', self.edit_tournament_info)]

        if len(self.tournament.rounds) == 0:
            menu.append(Option('Add/Remove tournament players', self.add_remove_tournament_players))

        if len(self.tournament.players) >= 2:
            if self.tournament.round_started:
                menu.append(Option(f'End round', self.end_round))
            elif len(self.tournament.rounds) < self.tournament.number_of_rounds:
                menu.append(Option('Start round', self.start_round))

        if len(self.tournament.players) > 0:
            menu.append(Option('Show players', self.display_players))

        menu.append(Option('Show all rounds', self.show_rounds))
        menu.append(Option('Show all matches', self.show_matches))

        menu.append(Option('Exit', self.exit))
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
        return True

    def serialize_tournament(self):
        serialized_tournament = {
            'name': self.tournament.name,
            'venue': self.tournament.venue,
            'date': self.tournament.date,
            'number_of_rounds': self.tournament.number_of_rounds,
            'rounds': self.tournament.serialize_rounds(),
            # 'rounds': list(map(lambda x: x.serialize_round, self.tournament.rounds)),
            'players': list(map(lambda x: x.id, self.tournament.players)),
            'time_control': self.tournament.time_control,
            'description': self.tournament.description,
            'round_started': self.tournament.round_started,
            'id': self.tournament.id
        }
        return serialized_tournament

    def get_tournament_from_db(self, serialized_tournament):
        rounds = []
        for serialized_round in serialized_tournament['rounds']:
            rounds.append(self.get_round_from_db(serialized_round))
        tournament = Tournament(name=serialized_tournament['name'],
                                venue=serialized_tournament['venue'],
                                date=serialized_tournament['date'],
                                number_of_rounds=serialized_tournament['number_of_rounds'],
                                time_control=serialized_tournament['time_control'],
                                description=serialized_tournament['description'],
                                rounds=rounds,
                                players=[x.player for x in self.player_controller.players
                                         if x.player.id in serialized_tournament['players']],
                                round_started=serialized_tournament['round_started'],
                                tournament_id=serialized_tournament['id'])
        return tournament

    def get_round_from_db(self, serialized_round):
        matches = []
        for [[player1_id, score1], [player2_id, score2]] in serialized_round['matches']:
            player1 = next(x.player for x in self.player_controller.players if x.player.id == player1_id)
            player2 = next(x.player for x in self.player_controller.players if x.player.id == player2_id)
            matches.append(([player1, score1], [player2, score2]))
        rnd = Round(name=serialized_round['name'],
                    matches=matches,
                    start_time=serialized_round['start_time'],
                    end_time=serialized_round['end_time'])
        return rnd
