class RoundView:
    # def __init__(self, round):
    #     self.round = round

    def display_pairings(self, pairings):
        print('Here are the pairings for the next round:')
        for player1, player2 in pairings:
            print(f'{player1.get_full_name()} -- {player2.get_full_name()}')

    def prompt_for_winner(self, pairings):
        """
        Gets round results from manager, for each pairing/player
        :param pairings: pairs of players for the round
        :return: a list containing the winning players or None, in case of a tie
        """
        print("Let's enter the results for this round:")
        results = []
        for players in pairings:
            winner_index = 0
            while winner_index not in [1, 2, 3]:
                try:
                    winner_index = int(input(f'Who won? \n'
                                             f'1. {players[0].get_full_name()}\n'
                                             f'2. {players[1].get_full_name()}\n'
                                             f'3. Tie \n'))
                    if winner_index not in [1, 2, 3]:
                        raise ValueError
                except ValueError:
                    print('Enter the number for the winner or 3 for a tie.')
                    continue
            match winner_index:
                case 3: results.append(None)
                case _: results.append(players[winner_index - 1])
        return results


from TestModel import TestPlayer
from Player import Player
PAIRINGS = [(Player(*TestPlayer().get_data()), Player(*TestPlayer().get_data())),
            (Player(*TestPlayer().get_data()), Player(*TestPlayer().get_data()))]
round = RoundView()
round.display_pairings(PAIRINGS)
for winner in round.prompt_for_winner(PAIRINGS):
    if winner is not None:
        print(winner.get_full_name())
    else:
        print("Tie game")
