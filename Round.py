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
        :param results: list of
        :return:

        """
        pass

    def get_pairings(self):
        pass

    def add_end_time(self):
        self.end_time = datetime.datetime.now()