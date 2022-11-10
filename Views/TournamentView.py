from Views.BaseView import BaseView


MINIMUM_OF_ROUNDS = 1
TIME_CONTROLS = ['Bullet', 'Blitz', 'Rapid']
DEFAULT_NUM_ROUNDS = 4


class TournamentView:
    def __init__(self):
        self.base_view = BaseView()

    def select_player(self, all_players, tournament_players):
        """
        Ask manager to select a player to add to or remove from the list
        of players in the tournament, or to create a new player and add it to
        the tournament. An empty answer stops the process
        :param all_players: a list of all Players saved in the system
        :param tournament_players: a list of Players part of the tournament
        :return : the index of player in all_players to add to or remove from
        the players in tournament.
        If return -1, create a new player.
        If return None, stop calling the function.
        """
        menu = []
        for i, player in enumerate(all_players):
            proposition = player.get_full_name()
            if player in tournament_players:
                proposition += ' [[ Selected ]]'
            menu.append(proposition)
        return self.base_view.select_from_list(menu, proposition_zero='Add a new player', cancel_allowed=True)

    def prompt_for_tournament_name(self):
        return self.base_view.prompt_for_text('name of the tournament')

    def prompt_for_venue(self):
        return self.base_view.prompt_for_text('name of the venue')

    def prompt_for_date_range(self):
        first_day = self.base_view.prompt_for_date('first day of the tournament')
        last_day = self.base_view.prompt_for_date('last day of the tournament')
        return first_day, last_day

    def prompt_for_number_rounds(self):
        return self.base_view.prompt_for_number('number of rounds', mini=MINIMUM_OF_ROUNDS, default=DEFAULT_NUM_ROUNDS)

    def prompt_for_time_control(self):
        return self.base_view.select_from_list(TIME_CONTROLS)

    def prompt_for_description(self):
        return self.base_view.prompt_for_text('tournament description')

    def get_new_name(self, tournament_name):
        print(f'The Tournament current name is {tournament_name}.')
        return self.base_view.prompt_for_text('new tournament name')

    def get_new_venue(self, tournament_name, current_name):
        print(f'The Tournament {tournament_name} current venue is {current_name}.')
        return self.base_view.prompt_for_text('tournament new venue')

    def get_new_date_range(self, tournament_name, current_date_range):
        print(f'The Tournament {tournament_name} current dates are: {current_date_range}.')
        first_day = self.base_view.prompt_for_date('new first day of the tournament')
        last_day = self.base_view.prompt_for_date('new last day of the tournament')
        return first_day, last_day

    def get_new_number_of_rounds(self, tournament_name, current_number):
        print(f'The Tournament {tournament_name} current number of rounds is {current_number}.')
        return self.base_view.prompt_for_number('new number of rounds',
                                                mini=MINIMUM_OF_ROUNDS,
                                                default=DEFAULT_NUM_ROUNDS)

    def get_new_time_control(self, tournament_name, current_time_control):
        print(f'The Tournament {tournament_name} current time control is {TIME_CONTROLS[current_time_control]}.')
        print('Select the new time control:')
        return self.base_view.select_from_list(TIME_CONTROLS)

    def get_new_description(self, tournament_name, current_description):
        print(f'The Tournament {tournament_name} current description is: \n{current_description}')
        return self.base_view.prompt_for_text('new tournament description')

    def get_new_last_name(self, player_name):
        return self.base_view.prompt_for_text(f"{player_name}'s new last name")

    def get_new_date_of_birth(self, player_name, date_of_birth):
        print(f"{player_name}'s current date of birth: {date_of_birth}.")
        return self.base_view.prompt_for_date("player's new date of birth")

    def display_pairings(self, pairs):
        for player1, player2 in pairs:
            print(player1.get_full_name(), ' - ', player2.get_full_name())

    def prompt_for_winner_index(self, pair):
        pair_of_names = list(map(lambda x: x.get_full_name(), pair))
        print('Who won?')
        winner_index = self.base_view.select_from_list(pair_of_names, proposition_zero='Tie Game')
        if winner_index == -1:
            return None
        return winner_index

    def display_rounds(self, rounds):
        if len(rounds) == 0:
            print('There is no round to show')
        else:
            print('  ## ROUNDS ##')
            for rnd in rounds:
                print(f'  # {rnd.name} #')
                for match_info in rnd.get_matches_info():
                    self.display_match(*match_info)

    def display_match(self, player1, score1, player2, score2):
        match_report = player1.get_full_name() + '  '
        if score1 == 0.5:
            match_report += '-TIE-'
        else:
            match_report += str(score1) + ' - ' + str(score2)
        match_report += '  ' + player2.get_full_name()
        print(match_report)

    def notice_no_more_pairings(self):
        print('All the players payed against each other, there is no more match to play in this tournament.')

    def notice_tournament_over(self):
        print('The tournament is now over.')
