import datetime


TIME_FORMAT = "%m/%d/%Y, %I:%M %p"


class Round:
    def __init__(self, name, pairings=None, matches=None,
                 start_time=datetime.datetime.now().strftime(TIME_FORMAT), end_time=None):
        self.name = name
        if matches is None:
            matches = []
            for player1, player2 in pairings:
                match = ([player1, 0], [player2, 0])
                matches.append(match)
        self.matches = matches
        self.start_time = start_time
        self.end_time = end_time

    #
    # Set Methods
    #
    def add_results(self, results):
        """Add results from a list of scores to each match in the round."""
        for i, match in enumerate(self.matches):
            match[0][1] = results[i][0]
            match[1][1] = results[i][1]

    def add_end_time(self):
        self.end_time = datetime.datetime.now().strftime(TIME_FORMAT)

    #
    # Get Methods
    #
    def get_pairs(self):
        """Return a list of all pairs of players in the round."""
        return list(map(lambda x: [x[0][0], x[1][0]], self.matches))

    def get_matches_info(self):
        """Return a list of tuples with player1, their score, player2, their score for each match in round."""
        info = []
        for [player1, score1], [player2, score2] in self.matches:
            info.append([player1, score1, player2, score2])
        return info

    def get_round_points(self, player):
        """Return a player's total number of points in this round."""
        points = 0
        for match in self.matches:
            if player == match[0][0]:
                points += match[0][1]
            if player == match[1][0]:
                points += match[1][1]
        return points

    def have_never_played(self, player1, player2):
        """Return whether two players played against each other during this round."""
        for [[p1, _], [p2, _]] in self.matches:
            if (player1 == p1 and player2 == p2) or (player1 == p2 and player2 == p1):
                return False
        return True

    #
    # Serialization Method
    #
    def serialize_round(self):
        """Return this round as a serialized round."""
        serialized_matches = []
        for [[player1, score1], [player2, score2]] in self.matches:
            serialized_matches.append([[player1.id, score1], [player2.id, score2]])
        return {'name': self.name,
                'matches': serialized_matches,
                'start_time': self.start_time,
                'end_time': self.end_time
                }
