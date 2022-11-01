class RoundController:
    def __init__(self, view, round):
        self.view = view
        self.round = round

    def start_round(self):
        """
        Get the list of 2-ple of players from ???tournament?
        and send the pairings to the view for display
        :param pairings: list of 2-ple containing Player objects
        :return: nothing
        """
        self.view.display_pairings(round.pairings)

    def end_round(self):
        """
        Ask for match results from manager (view)
        and send the scores to the round (model)
        :return: nothing
        """
        winners = self.view.prompt_for_winner(self.round.pairings)
        for i, pair in enumerate(self.round.pairings):
            self.assign_points(pair, winners[i])

    def assign_points(self, pair, winner):
        """
        Takes a pair of players and a winner, give 1 point to winner, 0 to loser
         and 0.5 each if there is no winner (None)
        :param pair: a 2-ple of players
        :param winner: a player
        :return: a tuple of 2 lists each containing a player and their score
        """
        if winner is None:
            self.round.matches.append([pair[0], 0.5], [pair[1], 0.5])
        if winner == pair[0]:
            self.round.matches.append([pair[0], 1], [pair[1], 0])
        if winner == pair[1]:
            self.round.matches.append([pair[0], 0], [pair[1], 1])


