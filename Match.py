class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0
        self.score2 = 0
        self.match_ended = False



    def get_result(self):
        if self.match_ended:
            return ([self.player1, self.score1],
                    [self.player2, self.score2])
        else:
            return None
