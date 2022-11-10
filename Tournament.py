from Round import Round


class Tournament:
    def __init__(self, name, venue, date_range, number_of_rounds,
                 time_control, description, rounds=None, players=None, round_started=False, tournament_id=None):
        self.name = name
        self.venue = venue
        self.date_range = date_range
        self.number_of_rounds = number_of_rounds
        if rounds is None:
            rounds = []
        self.rounds = rounds
        if players is None:
            players = []
        self.players = players
        self.time_control = time_control
        self.description = description
        self.round_started = round_started
        if tournament_id is None:
            self.id = self.__hash__()
        else:
            self.id = tournament_id

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_tournament_players(self, list_of_players=None):
        if list_of_players is None:
            list_of_players = self.players
        try:
            new_list = []
            for i in list_of_players:
                new_list.append(self.get_tournament_players(i))
            return new_list
        except TypeError:
            return list_of_players

    def start_new_round(self):
        this_round_number = len(self.rounds)
        if this_round_number < self.number_of_rounds:
            pairs = self.define_pairings(this_round_number)
            if pairs:
                round_name = 'Round ' + str(len(self.rounds) + 1)
                self.rounds.append(Round(name=round_name, pairings=pairs))
                self.round_started = True
            return self.get_tournament_players(pairs)

    def end_round(self, scores):
        this_round = self.rounds[-1]
        this_round.add_end_time()
        this_round.add_results(scores)
        self.round_started = False

    def has_ended(self):
        return len(self.rounds) == self.number_of_rounds and not self.round_started

    def get_round_pairs(self, round_index=-1):
        pairs = self.rounds[round_index].get_pairs()
        return self.get_tournament_players(pairs)

    def define_pairings(self, round_number):
        if round_number == 0:
            return self.first_round_pairing()
        else:
            return self.next_round_pairing()

    def first_round_pairing(self):
        tournament_players = self.players.copy()
        tournament_players.sort(key=lambda x: x.ranking, reverse=True)
        for player in tournament_players:
            print(f'Player: {player.get_full_name()}, ranking: {player.ranking}')
        half = len(tournament_players) // 2
        first_half = tournament_players[:half]
        second_half = tournament_players[half:]
        pairs = list(zip(first_half, second_half))
        return pairs

    def next_round_pairing(self):
        tournament_players = self.players.copy()

        def get_all_points(player_to_probe):
            points = 0
            for rnd in self.rounds:
                points += rnd.get_round_points(player_to_probe)
            return points

        tournament_players.sort(key=lambda x: (get_all_points(x), x.ranking), reverse=True)
        for player in tournament_players:
            print(f'Player: {player.get_full_name()}, points: {get_all_points(player)}, ranking: {player.ranking}')

        def get_all_pairs(players_left, new_pairs):
            def get_next_adversary(p1, *players):
                if not players:
                    return None
                p2, *other_players = players
                never_played = True
                for rnd in self.rounds:
                    never_played = never_played and rnd.have_never_played(p1, p2)
                if never_played:
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

    def serialize_rounds(self):
        serialized_rounds = []
        for rnd in self.rounds:
            serialized_rounds.append(rnd.serialize_round())
        return serialized_rounds
