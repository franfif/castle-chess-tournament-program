class SwissTournamentSystem:
    NAME = 'Swiss Tournament System'

    #
    # Pairing Methods - Swiss Tournament System
    #
    @staticmethod
    def define_pairings(round_number, tournament_players, tournament_rounds):
        """Return a list of pairs for a new round."""
        if round_number == 0:
            return SwissTournamentSystem.first_round_pairing(tournament_players)
        else:
            return SwissTournamentSystem.next_round_pairing(tournament_players, tournament_rounds)

    @staticmethod
    def first_round_pairing(tournament_players):
        """Return pairs of players for the first round."""
        # Sort players by their ranking
        tournament_players.sort(key=lambda x: x.ranking, reverse=True)
        # Divide the list of players in two lists
        half = len(tournament_players) // 2
        first_half = tournament_players[:half]
        second_half = tournament_players[half:]
        # Pair each player of the first half with the players of the second half
        pairs = list(zip(first_half, second_half))
        return pairs

    @staticmethod
    def next_round_pairing(tournament_players, tournament_rounds):
        """Return pairs of players for the rounds after the first round"""
        def get_all_points(player_to_probe, rounds):
            """Return the sum of a player's points from each round."""
            points = 0
            for rnd in rounds:
                points += rnd.get_round_points(player_to_probe)
            return points

        # Sort players by their total of points then by their ranking
        tournament_players.sort(key=lambda x: (get_all_points(x, tournament_rounds), x.ranking), reverse=True)

        def get_next_adversary(rounds, p1, *players):
            """Return the next adversary a player has not already played against in other rounds."""
            if not players:
                return None
            p2, *other_players = players
            never_played = True
            for rnd in rounds:
                never_played = never_played and rnd.have_never_played(p1, p2)
            if never_played:
                return p2
            else:
                return get_next_adversary(rounds, p1, *other_players)

        def get_all_pairs(players_left, new_pairs, rounds):
            """Find every player's next adversary in the round and return all the pairs."""
            if not players_left:
                return new_pairs
            else:
                player1 = players_left[0]
                player2 = get_next_adversary(rounds, *players_left)
                players_left.remove(player1)
                if player2 is not None:
                    players_left.remove(player2)
                    new_pairs.append([player1, player2])
                return get_all_pairs(players_left, new_pairs, rounds)

        return get_all_pairs(tournament_players, [], tournament_rounds)

    @staticmethod
    def serialize_tournament_system():
        return 'swiss_tournament_system'
