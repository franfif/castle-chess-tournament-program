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

    def add_player(self, player):
        self.players.append(TournamentPlayer(player))

    def remove_player(self, player):
        player_to_remove = next(x for x in self.players if x.player == player)
        self.players.remove(player_to_remove)

    def get_tournament_players(self):
        return list(map(lambda x: x.player, self.players))

    def reset_description(self, new_description):
        self.description = new_description

    def increment_description(self, new_line):
        self.description += '\n' + new_line

    def start_new_round(self):
        this_round = len(self.rounds)
        if this_round < self.number_of_rounds:
            round_name = 'Round ' + str(len(self.rounds) + 1)
            pairs = self.define_pairings(this_round)
            self.rounds.append(Round(round_name, pairs))
            self.save_pairs(pairs)
            return pairs

    def define_pairings(self, round_number):
        if round_number == 0:
            return self.first_round_pairing()
        else:
            return self.next_round_pairing()

    def first_round_pairing(self):
        tournament_players = list(self.players)
        tournament_players.sort(key=lambda x: x.player.ranking, reverse=True)
        half = len(tournament_players) // 2
        first_half = tournament_players[:half]
        second_half = tournament_players[half:]
        pairs = list(zip(first_half, second_half))
        return pairs

    def next_round_pairing(self):
        tournament_players = list(self.players)
        tournament_players.sort(key=lambda x: (x.points, x.player.ranking), reverse=True)
        if tournament_players[0].has_already_played(tournament_players[1]):
            pass
            # start again with [0] and [2]
        else:
            pass
            # pair [0] and [1]
            # remove [0] and [1] from ranked_players
            # start again with new ranked_players

    def save_pairs(self, pairs):
        for player1, player2 in pairs:
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
