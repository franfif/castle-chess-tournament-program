import datetime


class Round:
    def __init__(self, name, pairings):
        self.name = name
        self.matches = []
        for player1, player2 in pairings:
            match = ([player1, 0], [player2, 0])
            self.matches.append(match)
        self.start_time = datetime.datetime.now()
        self.end_time = None

    def add_results(self, results):
        """
        Add results for each match/pairing in the round
        :param results: list of lists of 2 scores
        :return: None
        """
        for i, [[player1, _], [player2, _]] in enumerate(self.matches):
            player1.points += results[i][0]
            player2.points += results[i][1]
            self.matches[i][0][1] = results[i][0]
            self.matches[i][1][1] = results[i][1]

    def get_pairs(self):
        return list(map(lambda x: [x[0][0].player, x[1][0].player], self.matches))

    def add_end_time(self):
        self.end_time = datetime.datetime.now()
