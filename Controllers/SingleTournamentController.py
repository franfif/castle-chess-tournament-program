from Views.TournamentView import TournamentView
from Models.Tournament import Tournament
from Models.Option import Option
from Views.BaseView import BaseView
from Models.Round import Round
from Models.Message import Message
from Models.MenuManager import MenuManager
from Models.SwissTournamentSystem import SwissTournamentSystem


class SingleTournamentController:
    def __init__(self, players_control, tournaments_control, tournament_system=None, tournament_info=None):
        self.players_control = players_control
        self.tournaments_control = tournaments_control
        self.view = TournamentView()
        self.base_view = BaseView()
        if tournament_info is not None:
            self.tournament = self.deserialize_tournament(tournament_info)
        else:
            self.tournament = Tournament(tournament_system, *self.get_tournament_info())

    def get_tournament_info(self):
        name = self.view.prompt_for_tournament_name()
        venue = self.view.prompt_for_venue()
        date_range = self.view.prompt_for_date_range()
        number_of_rounds = self.view.prompt_for_number_rounds()
        time_control = self.view.prompt_for_time_control()
        description = self.view.prompt_for_description()
        return name, venue, date_range, number_of_rounds, time_control, description

    #
    # Run Tournament Menu and Options
    #
    def run(self):
        """Send a list of Options to MenuManager to allow user to run the tournament."""
        MenuManager.menu(get_options_method=self.run_tournament_options,
                         save_method=self.tournaments_control.save_tournaments_to_db,
                         titles=(Message.ONGOING_TOURNAMENT_MENU, self.tournament.name))

    def run_tournament_options(self):
        options = [Option(Message.EDIT_TOURNAMENT, self.edit_tournament)]

        if len(self.tournament.rounds) == 0:
            options.append(Option(Message.ADD_REMOVE_TOURNAMENT_PLAYERS, self.add_remove_tournament_players))

        if len(self.tournament.players) >= 2:
            if self.tournament.round_started:
                options.append(Option(Message.END_TOURNAMENT_ROUND, self.end_round))
            elif len(self.tournament.rounds) < self.tournament.number_of_rounds:
                options.append(Option(Message.START_TOURNAMENT_ROUND, self.start_round))

        if len(self.tournament.players) > 0:
            options.append(Option(Message.SHOW_PLAYERS, self.show_players))

        options.append(Option('Show all rounds', self.show_rounds))
        options.append(Option.exit_option(saving=True))
        return options

    #
    # Edit Tournament Menu and Options
    #
    def edit_tournament(self):
        """Send edit Options to MenuManager to allow user to edit the tournament."""
        MenuManager.menu(get_options_method=self.edit_tournament_options,
                         save_method=self.tournaments_control.save_tournaments_to_db,
                         titles=(Message.ONGOING_TOURNAMENT_MENU, self.tournament.name))

    def edit_tournament_options(self):
        options = [Option(Message.UPDATE_TOURNAMENT_NAME, self.update_tournament_name),
                   Option(Message.UPDATE_VENUE, self.update_venue),
                   Option(Message.UPDATE_DATES, self.update_dates),
                   Option(Message.UPDATE_NUMBER_OF_ROUNDS, self.update_number_of_rounds),
                   Option(Message.UPDATE_TIME_CONTROL, self.update_time_control),
                   Option(Message.UPDATE_DESCRIPTION, self.update_description),
                   Option.exit_option(saving=True)]
        return options

    #
    # Report Menu and Options
    #
    def run_reports(self):
        """Send tournament report options to the MenuManager."""
        MenuManager.menu(get_options_method=self.report_options,
                         titles=(Message.ONGOING_TOURNAMENT_MENU, self.tournament.name),
                         content=(self.view.display_tournament_info, self.tournament))

    def report_options(self):
        options = [Option(Message.SHOW_PLAYERS, self.show_players),
                   Option(Message.SHOW_ROUNDS, self.show_rounds),
                   Option.exit_option()]
        return options

    #
    # Run Tournament Methods
    #
    def add_remove_tournament_players(self):
        """Add and remove players from tournament according to user's choice."""
        while True:
            all_players = self.get_all_players()
            titles = (Message.TOURNAMENTS_TITLE, self.tournament.name, Message.SELECT_PLAYERS)
            # Fetch selection from user
            index = self.view.select_player(all_players=all_players,
                                            tournament_players=self.tournament.players,
                                            titles=titles)
            if index is None:
                # User has not selected any player, stop the process
                break
            elif index == -1:
                # Create new player and add it to tournament players
                self.players_control.create_player()
                all_players = self.get_all_players()
                self.tournament.add_player(all_players[index])
            elif all_players[index] in self.tournament.players:
                # Remove player from tournament
                self.tournament.remove_player(all_players[index])
            else:
                # Add player to tournament
                self.tournament.add_player(all_players[index])
            self.tournaments_control.save_tournaments_to_db()

    def get_all_players(self):
        return list(map(lambda x: x.player, self.players_control.players))

    def start_round(self):
        """Display pairs for new round or end the tournament if no more pairs."""
        # Get the pairs from the tournament
        pairs = self.tournament.start_new_round()
        if pairs:
            # Display pairs to user
            MenuManager.menu(get_options_method=self.exit_only_option,
                             titles=(Message.ONGOING_TOURNAMENT_MENU,
                                     self.tournament.name,
                                     Message.STARTING + self.tournament.rounds[-1].name),
                             content=(self.view.display_pairings, pairs))
        else:
            # no more pair possible, so end the tournament
            self.view.send_notice(Message.NO_MORE_PAIRINGS)
            self.end_tournament()

    def end_round(self):
        """Fetch result for each match in the round and add them to the round instance."""
        # Get the current round's pairs
        pairs = self.tournament.get_round_pairs()
        # Attribute points to each match in the round
        scores = []
        for i, pair in enumerate(pairs):
            BaseView.display_titles((Message.ONGOING_TOURNAMENT_MENU,
                                     self.tournament.name,
                                     Message.ENDING + self.tournament.rounds[-1].name))
            # For each pair, get the winner index from view
            winner_index = self.view.prompt_for_winner_index(pair)
            # Collect scores for each pairs
            scores.append(self.attribute_score(winner_index))
        # Apply scores to round to end the round
        self.tournament.end_round(scores)
        # End tournament if this was the last round
        if self.tournament.number_of_rounds == len(self.tournament.rounds):
            self.end_tournament()

    @staticmethod
    def attribute_score(winner_index):
        score = [0.5, 0.5]
        if winner_index is not None:
            score[winner_index] = 1
            score[1 - winner_index] = 0
        return score

    def end_tournament(self):
        self.tournament.number_of_rounds = len(self.tournament.rounds)
        self.view.send_notice(Message.TOURNAMENT_OVER)

    #
    # Edit Tournament Methods
    #
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

    #
    # Report Tournament Methods
    #
    def show_tournament_info(self):
        """Send tournament info for MenuManager to display."""
        MenuManager.menu(get_options_method=self.exit_only_option,
                         titles=(Message.REPORT_MENU,
                                 Message.ONGOING_TOURNAMENT_MENU,
                                 self.tournament.name),
                         content=(self.view.display_tournament_info, self.tournament))

    def show_players(self):
        """Send tournament players for MenuManager to display."""
        players = self.players_control.get_players_in_preferred_order(self.tournament.players)
        MenuManager.menu(get_options_method=self.exit_only_option,
                         titles=(Message.REPORT_MENU,
                                 Message.ONGOING_TOURNAMENT_MENU,
                                 self.tournament.name,
                                 Message.PLAYERS_TITLE),
                         content=(self.players_control.view.display_players, players))

    def show_rounds(self):
        """Send tournament rounds info for MenuManager to display."""
        MenuManager.menu(get_options_method=self.exit_only_option,
                         titles=(Message.REPORT_MENU,
                                 Message.ONGOING_TOURNAMENT_MENU,
                                 self.tournament.name,
                                 Message.ROUNDS_TITLE),
                         content=(self.view.display_rounds, self.tournament.rounds))

    @staticmethod
    def exit_only_option():
        return [Option.exit_option()]

    #
    # Serialization - Deserialization Methods
    #
    def serialize_tournament(self):
        """Return this tournament as a serialized tournament."""
        serialized_tournament = {
            'tournament_system': self.tournament.tournament_system.serialize_tournament_system(),
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

    def deserialize_tournament(self, serialized_tournament):
        """Return a Tournament object from a serialized tournament."""
        rounds = []
        # Get a list of Round objects from a list of serialized rounds
        for serialized_round in serialized_tournament['rounds']:
            rounds.append(self.deserialized_round(serialized_round))

        tournament = Tournament(tournament_system=self.deserialized_tournament_system(
            serialized_tournament['tournament_system']),
                                name=serialized_tournament['name'],
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

    def deserialized_round(self, serialized_round):
        """Return a Round object from a serialized round."""
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

    @staticmethod
    def deserialized_tournament_system(serialized_tournament_system):
        if serialized_tournament_system == 'swiss_tournament_system':
            return SwissTournamentSystem()
