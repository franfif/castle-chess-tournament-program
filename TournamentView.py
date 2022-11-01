from BaseView import BaseView
MINIMUM_OF_ROUNDS = 1
TIME_CONTROLS = ['Bullet', 'Blitz', 'Rapid']


class TournamentView:
    def __init__(self):
        self.base_view = BaseView()

    def select_player(self, all_players, tournament_players):
        """
        Ask manager to select a player to add to or remove from the list
        of players in the tournament, or to create a new player and add it to
        the tournament.
        An empty answer stops the process
        :param all_players: a list of all players saved in the system
        :param tournament_players: a list of players part of the tournament
        :return : the index of player in all_players to add to or remove from
        the players in tournament.
        If return -1, create a new player.
        If return None, stop calling the function.
        """
        menu = []
        for i, player in enumerate(all_players):
            proposition = player.get_full_name()
            if player in tournament_players:
                proposition += " [[ Selected ]]"
            menu.append(proposition)
        proposition_zero = 'Add a new player'
        return self.base_view.select_from_list(menu, proposition_zero)

    def prompt_for_tournament_name(self):
        return self.base_view.prompt_for_text('name of the tournament')

    def prompt_for_venue(self):
        return self.base_view.prompt_for_text('name of the venue')

    def prompt_for_date_range(self):
        first_day = self.base_view.prompt_for_date('first day of the tournament')
        last_day = self.base_view.prompt_for_date('last day of the tournament')
        return first_day, last_day

    def prompt_for_number_rounds(self):
        return self.base_view.prompt_for_number("number of rounds", mini=MINIMUM_OF_ROUNDS)

    def prompt_for_time_control(self):
        return self.base_view.select_from_list(TIME_CONTROLS)

    def prompt_for_description(self):
        return self.base_view.prompt_for_text("tournament description")

    def display_pairings(self, pairs):
        pass

    def prompt_for_winners(self, matches):
        winners = []
        for match in matches:
            print('Who won?')
            winner_index = self.base_view.select_from_list(match, "Tie Game", cancel_allowed=False)
            if winner_index == -1:
                winner_index = None
            winners.append(match[winner_index])
        return winners

    def show_players(self, players):
        if len(players) == 0:
            print("No players to show.")
        else:
            print("How would you like to order the players?")
            choices = ['ranking', 'alphabetical']
            choice = self.base_view.select_from_list(choices, cancel_allowed=False)
            order = choices[choice]
            print(f"Players in the tournament in {order} order:")
            if order == 'ranking':
                players = self.base_view.order_by_ranking(players)
            else:
                players = self.base_view.order_alphabetically(players)
            for player in players:
                self.base_view.full_display_player(player)

    def display_rounds(self, rounds):
        if len(rounds) == 0:
            print('There is no round to show')
        else:
            for round in rounds:
                print(round.name)
                for match in round:
                    player1 = match[0][0]
                    score1 = match[0][1]
                    player2 = match[1][0]
                    score2 = match[1][1]
                    match_report = player1.get_full_name() + '  '
                    if score1 == 0.5:
                        match_report += '-TIE-'
                    else:
                        match_report += score1 + ' - ' + score2
                    match_report += player2.get_full_name()
                    print(match_report)
