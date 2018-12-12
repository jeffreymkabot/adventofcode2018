import sys
from collections import deque

class Game:
    n_players = 0

    turn = 0
    scores = {}
    # originally used a list and kept track of current marble using a separate cursor variable
    # but for part two
    # the time cost of moving memory on list.insert(i) / list.pop(i) became too high
    # https://wiki.python.org/moin/TimeComplexity
    circle = deque([0])

    def __init__(self, n_players):
        self.n_players = n_players

    def __iter__(self):
        return self

    def __next__(self):
        self.turn += 1
        player = self.turn % self.n_players
        marble = self.turn

        if marble % 23 == 0:
            self.circle.rotate(-7)
            other_marble = self.circle.pop()
            self.scores[player] = self.scores.get(player, 0) + marble + other_marble
            return self.scores.copy()

        self.circle.rotate(2)
        self.circle.append(marble)
        return self.scores.copy()

def main():
    n_players = 9
    turns = 25
    if len(sys.argv) >= 2:
        n_players = int(sys.argv[1])
    if len(sys.argv) >= 3:
        turns = int(sys.argv[2])

    game = Game(n_players)
    for x in range(turns):
        score = next(game)

    result = max(score.values())
    print('Winning score', result)

if __name__ == '__main__':
    main()
