class TournamentPlayer:
    def __init__(self, player):
        self.player = player
        self.points = 0
        self.pairs = []

    def has_never_played(self, other_player):
        return other_player not in self.pairs

    def is_now_playing(self, other_player):
        self.pairs.append(other_player)
