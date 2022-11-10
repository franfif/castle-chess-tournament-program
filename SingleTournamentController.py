from TournamentView import TournamentView
from Tournament import Tournament
from Option import Option
from BaseView import BaseView
from Round import Round


class SingleTournamentController:
    def __init__(self, players_control, tournaments_control, tournament_info=None):
        self.players_control = players_control
        self.tournaments_control = tournaments_control
        self.view = TournamentView()
        self.base_view = BaseView()
        self.all_players = list(map(lambda x: x.player, self.players_control.players))
        if tournament_info is not None:
            if isinstance(tournament_info, tuple):
                self.tournament = Tournament(*tournament_info)
            else:
                self.tournament = self.get_tournament_from_db(tournament_info)
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
            index = self.view.select_player(self.all_players, self.tournament.players)
            if index is None:
                # stop the process
                break
            elif index == -1:
                # create new player and add it to tournament players
                self.players_control.create_player()
                self.tournament.add_player(self.all_players[index])
            elif self.all_players[index] in self.tournament.players:
                # remove player
                self.tournament.remove_player(self.all_players[index])
            else:
                # add player
                self.tournament.add_player(self.all_players[index])
            self.tournaments_control.save_tournaments_to_db()

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
        self.players_control.display_players(self.tournament.players)

    def run(self):
        next_action = None
        while next_action is None:
            self.base_view.display_title('Tournament ' + self.tournament.name)
            menu = self.run_tournament_options()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.base_view.select_from_list(menu_names)
            next_action = menu[to_do].function()
            self.tournaments_control.save_tournaments_to_db()
        return

    def run_tournament_options(self):
        options = [Option('Edit tournament information', self.edit_tournament_info)]

        if len(self.tournament.rounds) == 0:
            options.append(Option('Add/Remove tournament players', self.add_remove_tournament_players))

        if len(self.tournament.players) >= 2:
            if self.tournament.round_started:
                options.append(Option(f'End round', self.end_round))
            elif len(self.tournament.rounds) < self.tournament.number_of_rounds:
                options.append(Option('Start round', self.start_round))

        if len(self.tournament.players) > 0:
            options.append(Option('Show players', self.display_players))

        options.append(Option('Show all rounds', self.show_rounds))
        options.append(Option('Show all matches', self.show_matches))

        options.append(Option('Exit', self.exit))
        return options

    def edit_tournament_info(self):
        next_action = None
        while next_action is None:
            menu = self.edit_tournament_options()
            menu_names = list(map(lambda x: x.name, menu))
            to_do = self.base_view.select_from_list(menu_names)
            next_action = menu[to_do].function()
            self.tournaments_control.save_tournaments_to_db()
        return

    def edit_tournament_options(self):
        options = [Option('Change tournament name', self.update_tournament_name),
                   Option('Change venue', self.update_venue),
                   Option('Change dates', self.update_dates),
                   Option('Change number of rounds', self.update_number_of_rounds),
                   Option('Change time control', self.update_time_control),
                   Option('Change description', self.update_description),
                   Option('Save and go back', self.exit)]
        return options

    def update_tournament_name(self):
        new_name = self.view.get_new_name(self.tournament.name)
        self.tournament.name = new_name

    def update_venue(self):
        new_venue = self.view.get_new_venue(self.tournament.name, self.tournament.venue)
        self.tournament.venue = new_venue

    def update_dates(self):
        new_date_range = self.view.get_new_date_range(self.tournament.name,
                                                      self.tournament.date_range)
        self.tournament.date_range = new_date_range

    def update_number_of_rounds(self):
        new_number_of_rounds = self.view.get_new_number_of_rounds(self.tournament.name,
                                                                  self.tournament.number_of_rounds)
        self.tournament.number_of_rounds = new_number_of_rounds

    def update_time_control(self):
        new_time_control = self.view.get_new_time_control(self.tournament.name,
                                                          self.tournament.time_control)
        self.tournament.time_control = new_time_control

    def update_description(self):
        new_description = self.view.get_new_description(self.tournament.name,
                                                        self.tournament.description)
        self.tournament.description = new_description

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
            'date': self.tournament.date_range,
            'number_of_rounds': self.tournament.number_of_rounds,
            'rounds': self.tournament.serialize_rounds(),
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
                                date_range=serialized_tournament['date'],
                                number_of_rounds=serialized_tournament['number_of_rounds'],
                                time_control=serialized_tournament['time_control'],
                                description=serialized_tournament['description'],
                                rounds=rounds,
                                players=[x.player for x in self.players_control.players
                                         if x.player.id in serialized_tournament['players']],
                                round_started=serialized_tournament['round_started'],
                                tournament_id=serialized_tournament['id'])
        return tournament

    def get_round_from_db(self, serialized_round):
        matches = []
        for [[player1_id, score1], [player2_id, score2]] in serialized_round['matches']:
            player1 = next(x.player for x in self.players_control.players if x.player.id == player1_id)
            player2 = next(x.player for x in self.players_control.players if x.player.id == player2_id)
            matches.append(([player1, score1], [player2, score2]))
        rnd = Round(name=serialized_round['name'],
                    matches=matches,
                    start_time=serialized_round['start_time'],
                    end_time=serialized_round['end_time'])
        return rnd
