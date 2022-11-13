from Models.Round import Round


class Tournament:
    def __init__(self, tournament_system, name, venue, date_range, number_of_rounds, time_control, description,
                 rounds=None, players=None, round_started=False, tournament_id=None):
        self.tournament_system = tournament_system
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
            tournament_id = self.__hash__()
        self.id = tournament_id

    #
    # Update Players
    #
    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    #
    # Update Rounds
    #
    def start_new_round(self):
        """Return the pairs of the new round or an empty list."""
        this_round_number = len(self.rounds)
        if this_round_number < self.number_of_rounds:
            pairs = self.define_pairings(this_round_number)
            if pairs:
                round_name = 'Round ' + str(len(self.rounds) + 1)
                self.rounds.append(Round(name=round_name, pairings=pairs))
                self.round_started = True
            return pairs

    def end_round(self, scores):
        """Update round's end_time and results"""
        this_round = self.rounds[-1]
        this_round.add_end_time()
        this_round.add_results(scores)
        self.round_started = False

    def has_ended(self):
        return len(self.rounds) == self.number_of_rounds and not self.round_started

    def get_round_pairs(self, round_index=-1):
        pairs = self.rounds[round_index].get_pairs()
        return pairs

    #
    # Serialization Method
    #
    def serialize_rounds(self):
        """Return a list of this tournament's serialized rounds."""
        serialized_rounds = []
        for rnd in self.rounds:
            serialized_rounds.append(rnd.serialize_round())
        return serialized_rounds
