from views.base_view import BaseView


MINIMUM_OF_ROUNDS = 1
TIME_CONTROLS = ['Bullet', 'Blitz', 'Rapid']
DEFAULT_NUM_ROUNDS = 4


class TournamentView(BaseView):
    def __init__(self):
        super().__init__()

    #
    # Original Input Methods
    #
    def prompt_for_tournament_name(self):
        return self.prompt_for_text('name of the tournament')

    def prompt_for_venue(self):
        return self.prompt_for_text('name of the venue')

    def prompt_for_date_range(self):
        first_day = self.prompt_for_date('first day of the tournament')
        last_day = self.prompt_for_date('last day of the tournament')
        return first_day, last_day

    def prompt_for_number_rounds(self):
        return self.prompt_for_number('number of rounds', mini=MINIMUM_OF_ROUNDS, default=DEFAULT_NUM_ROUNDS)

    def prompt_for_time_control(self):
        print('Select the time control:')
        return self.select_from_list(TIME_CONTROLS)

    def prompt_for_description(self):
        return self.prompt_for_text('tournament description')

    #
    # Update Input Methods
    #
    def get_new_name(self, tournament_name):
        print(f'The Tournament current name is {tournament_name}.')
        return self.prompt_for_text('new tournament name')

    def get_new_venue(self, tournament_name, current_name):
        print(f'The Tournament {tournament_name} current venue is {current_name}.')
        return self.prompt_for_text('tournament new venue')

    def get_new_date_range(self, tournament_name, current_date_range):
        print(f'The Tournament {tournament_name} current dates are: {current_date_range}.')
        first_day = self.prompt_for_date('new first day of the tournament')
        last_day = self.prompt_for_date('new last day of the tournament')
        return first_day, last_day

    def get_new_number_of_rounds(self, tournament_name, current_number):
        print(f'The Tournament {tournament_name} current number of rounds is {current_number}.')
        return self.prompt_for_number('new number of rounds',
                                      mini=MINIMUM_OF_ROUNDS,
                                      default=DEFAULT_NUM_ROUNDS)

    def get_new_time_control(self, tournament_name, current_time_control):
        print(f'The Tournament {tournament_name} current time control is {TIME_CONTROLS[current_time_control]}.')
        print('Select the new time control:')
        return self.select_from_list(TIME_CONTROLS)

    def complete_description(self, tournament_name, current_description):
        print(f'The Tournament {tournament_name} current description is: \n{current_description}')
        return self.prompt_for_text('description complement to add to the current description')

    def get_new_description(self, tournament_name, current_description):
        print(f'The Tournament {tournament_name} current description is: \n{current_description}')
        return self.prompt_for_text('new tournament description')

    #
    # Choice Input Methods
    #
    def select_player(self, all_players, tournament_players, titles):
        """Display all players for user to select or unselect, return selected list
        :param all_players: a list of all Players saved in the system
        :param tournament_players: a list of Players part of the tournament
        :param titles: a tuple of titles to display before the selection
        :return : the index of player in all_players to add to or remove from
        the players in tournament.
        """
        self.display_titles(titles)
        menu = []
        for i, player in enumerate(all_players):
            option = player.get_full_name()
            if player in tournament_players:
                option += ' [[ Participant ]]'
            menu.append(option)
        return self.select_from_list(menu, option_zero='Add a new player', cancel_allowed=True)

    def prompt_for_winner_index(self, pair):
        """Display players of each match and return index of the winner."""
        pair_of_names = list(map(lambda x: x.get_full_name(), pair))
        print('Who won?')
        winner_index = self.select_from_list(pair_of_names, option_zero='Tie Game')
        if winner_index == -1:
            return None
        return winner_index

    #
    # Display Methods
    #
    @staticmethod
    def display_pairings(pairs):
        for player1, player2 in pairs:
            print(player1.get_full_name(), ' - ', player2.get_full_name())

    def display_rounds(self, rounds):
        if len(rounds) == 0:
            print('There is no round to show')
        else:
            for rnd in rounds:
                print(f'  # {rnd.name} #')
                print(f'Started on {rnd.start_time} - '
                      f'{f"Ended on {rnd.end_time}" if rnd.end_time else "Not ended"}')
                for match_info in rnd.get_matches_info():
                    self.display_match(*match_info)
                print('')

    @staticmethod
    def display_match(player1, score1, player2, score2):
        match_report = player1.get_full_name() + '  '
        if score1 == 0.5:
            match_report += '-TIE-'
        else:
            match_report += str(score1) + ' - ' + str(score2)
        match_report += '  ' + player2.get_full_name()
        print(match_report)

    @staticmethod
    def display_tournament_info(tournament):
        print(f'Name: {tournament.name} \n'
              f'Tournament System: {tournament.tournament_system.NAME} \n'
              f'Venue: {tournament.venue} \n'
              f'Dates: {tournament.date_range[0]} - {tournament.date_range[1]} \n'
              f'Number of rounds: {tournament.number_of_rounds} \n'
              f'Number of rounds done: {len(tournament.rounds)} \n'
              f'Time Control: {TIME_CONTROLS[tournament.time_control]} \n'
              f'Description: {tournament.description} \n')
