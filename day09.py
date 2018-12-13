"""
--- Day 9: Marble Mania ---
You talk to the Elves while you wait for your navigation system to initialize. To pass the time, they introduce you to their favorite marble game.

The Elves play this game by taking turns arranging the marbles in a circle according to very particular rules. The marbles are numbered starting with 0 and increasing by 1 until every marble has a number.

First, the marble numbered 0 is placed in the circle. At this point, while it contains only a single marble, it is still a circle: the marble is both clockwise from itself and counter-clockwise from itself. This marble is designated the current marble.

Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that there is one marble between the marble that was just placed and the current marble.) The marble that was just placed then becomes the current marble.

However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens. First, the current player keeps the marble they would have placed, adding it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score. The marble located immediately clockwise of the marble that was removed becomes the new current marble.

For example, suppose there are 9 players. After the marble with value 0 is placed in the middle, each player (shown in square brackets) takes a turn. The result of each of those turns would produce circles of marbles like this, where clockwise is to the right and the resulting current marble is in parentheses:

[-] (0)
[1]  0 (1)
[2]  0 (2) 1 
[3]  0  2  1 (3)
[4]  0 (4) 2  1  3 
[5]  0  4  2 (5) 1  3 
[6]  0  4  2  5  1 (6) 3 
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7 
[9]  0  8  4 (9) 2  5  1  6  3  7 
[1]  0  8  4  9  2(10) 5  1  6  3  7 
[2]  0  8  4  9  2 10  5(11) 1  6  3  7 
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7 
[4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7 
[5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7 
[6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
[7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15 
[8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15 
[9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15 
[1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15 
[2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15 
[3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15 
[4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15 
[5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15
[6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15 
[7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15
The goal is to be the player with the highest score after the last marble is used up. Assuming the example above ends after the marble numbered 25, the winning score is 23+9=32 (because player 5 kept marble 23 and removed marble 9, while no other player got any points in this very short example game).

Here are a few more examples:

10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
What is the winning Elf's score?

--- Part Two ---
Amused by the speed of your answer, the Elves are curious:

What would the new winning Elf's score be if the number of the last marble were 100 times larger?

"""
import re
import numpy as np
from typing import Iterator


def circular_iterator(n: int) -> Iterator:
    while True:
        for i in range(1, n+1):
            yield i


class Game:
    def __init__(self, num_players: int, num_marbles: int) -> None:
        self.num_players = num_players
        self.num_marbles = num_marbles
        self.board = [0]
        self.available_marbles = list(range(1, num_marbles))
        self.current_idx = 0
        self.current_marble = 0
        self.points = {n: 0 for n in range(1, num_players+1)}
        self.finished = False

    @staticmethod
    def from_sentence(sentence: str) -> "Game":
        rgx = "([0-9]+) players; last marble is worth ([0-9]+) points"
        num_players, max_score = re.match(rgx, sentence).groups()
        return Game(
            num_players=int(num_players),
            num_marbles=int(max_score)+1,
        )

    def play(self):
        for self.player in circular_iterator(self.num_players):
            if not self.finished:
                self._play_turn()
            else:
                break

    def _play_turn(self) -> None:
        marble = self._get_lowest_marble()
        if marble % 23 != 0:
            self._place_standard(marble)
        else:
            self._place_special(marble)

    def _get_lowest_marble(self) -> None:
        marble = min(self.available_marbles)
        self.available_marbles.remove(marble)
        if not self.available_marbles:
            self.finished = True
        return marble

    # [4 5 6 7 8 9 ]
    #      c 1 2
    def _place_standard(self, marble: int) -> None:
        where = (self.current_idx + 2) % len(self.board)
        self.board.insert(where, marble)
        self.current_marble = marble
        self.current_idx = where

    def _place_special(self, marble: int) -> None:
        assert marble % 23 == 0
        # the current player keeps the marble they would have placed
        # adding it to their score
        self.points[self.player] += marble
        # the marble 7 marbles counter-clockwise from the current marble is removed from the circle
        extra_idx = (self.current_idx - 7) % len(self.board)
        extra = self.board[extra_idx]
        self.board.remove(extra)
        # and also added to the current player's score
        self.points[self.player] += extra
        # The marble located immediately clockwise of the marble that was removed becomes the new current marble
        self.current_idx = extra_idx
        self.current_marble = self.board[extra_idx]


RAW_TESTS = """10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305"""


def max_points(question: str) -> int:
    game = Game.from_sentence(question)
    game.play()
    return max(game.points.values())


# test cases for part 1
for TEST in RAW_TESTS.split("\n"):
    question, answer = TEST.split(": high score is ")
    assert int(answer) == max_points(question)

# part 1
print(max_points("429 players; last marble is worth 70901 points"))

# part 2
# This will take forever, I need a different implementation
print(max_points("429 players; last marble is worth 7090100 points"))
