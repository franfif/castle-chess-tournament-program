from Round import Round
from TournamentPlayer import TournamentPlayer


class Tournament:
    def __init__(self, name, venue, date, number_of_rounds,
                 time_control, description):
        self.name = name
        self.venue = venue
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.rounds = []
        self.players = []
        self.time_control = time_control
        self.description = description
        self.round_started = False

    def add_player(self, player):
        self.players.append(TournamentPlayer(player))

    def remove_player(self, player):
        """
        Remove an instance of TournamentPlayer from the tournament
        :param player: instance of Player
        :return: Nothing
        """
        player_to_remove = next(x for x in self.players if x.player == player)
        self.players.remove(player_to_remove)

    def get_tournament_players(self, list_of_players=None):
        """
        Gets through a list of TournamentPlayers and returns a list of corresponding Players
        :param list_of_players: list of TournamentPlayers. Default is the tournament's full list of TournamentPlayers
        :return: list of Players
        """
        if list_of_players is None:
            list_of_players = self.players
        try:
            new_list = []
            for i in list_of_players:
                new_list.append(self.get_tournament_players(i))
            return new_list
        except TypeError:
            return list(map(lambda x: x.player, list_of_players))

    def reset_description(self, new_description):
        self.description = new_description

    def increment_description(self, new_line):
        self.description += '\n' + new_line

    def start_new_round(self):
        this_round_number = len(self.rounds)
        if this_round_number < self.number_of_rounds:
            pairs = self.define_pairings(this_round_number)
            if pairs:
                round_name = 'Round ' + str(len(self.rounds) + 1)
                self.rounds.append(Round(round_name, pairs))
                self.save_pairs(pairs)
                self.round_started = True
            return pairs

    def end_round(self, scores):
        this_round = self.rounds[-1]
        this_round.add_results(scores)
        self.round_started = False

    def get_round_pairs(self, round_index=-1):
        return self.rounds[round_index].get_pairs()

    def define_pairings(self, round_number):
        if round_number == 0:
            return self.first_round_pairing()
        else:
            return self.next_round_pairing()

    def first_round_pairing(self):
        tournament_players = self.players.copy()
        tournament_players.sort(key=lambda x: x.player.ranking, reverse=True)
        half = len(tournament_players) // 2
        first_half = tournament_players[:half]
        second_half = tournament_players[half:]
        pairs = list(zip(first_half, second_half))
        return pairs

    def next_round_pairing(self):
        tournament_players = self.players.copy()
        tournament_players.sort(key=lambda x: (x.points, x.player.ranking), reverse=True)

        def get_all_pairs(players_left, new_pairs):
            def get_next_adversary(p1, *players):
                if not players:
                    return None
                p2, *other_players = players
                if p1.has_never_played(p2):
                    return p2
                else:
                    return get_next_adversary(p1, *other_players)

            if not players_left:
                return new_pairs
            else:
                player1 = players_left[0]
                player2 = get_next_adversary(*players_left)
                players_left.remove(player1)
                if player2 is not None:
                    players_left.remove(player2)
                    new_pairs.append([player1, player2])
                return get_all_pairs(players_left, new_pairs)

        return get_all_pairs(tournament_players, [])

    def save_pairs(self, pairs):
        for player1, player2 in pairs:
            if player2 is not None:
                player1.is_now_playing(player2)
                player2.is_now_playing(player1)

    # def already_done(self, possible_pair):
    #     for pair in self.pairs:
    #         if pair == possible_pair:
    #             return True
    #     return False

# TESTS
        # print('players')
        # for player in self.players:
        #     print(player.get_full_name())
        # print('ranked players')
        # for player in ranked_players:
        #     print(player.get_full_name())
        # print('first half')
        # for player in first_half:
        #     print(player.get_full_name())
        # print('second half')
        # for player in second_half:
        #     print(player.get_full_name())
        # print('pairs')
        # for pair in pairs:
        #     print(pair[0].get_full_name(),
        #           pair[1].get_full_name())
        #
