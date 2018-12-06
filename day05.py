import string
"""
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? 

"""
TEST = "dabAcCaCBAcCcaDA"

# These are the pairs of letters that can react
PAIRS1 = [a+A for a, A in zip(string.ascii_lowercase, string.ascii_uppercase)]
PAIRS2 = [A+a for a, A in zip(string.ascii_lowercase, string.ascii_uppercase)]
PAIRS = PAIRS1 + PAIRS2


class Polymer:
    def __init__(self, initial_config: str):
        self.initial_config = initial_config
        self.config = initial_config
        self.can_react = True

    def react(self):
        while self.can_react:
            self._react_once()

    def _react_once(self):
        """Make the polymer react once"""
        prev_config = self.config
        for pair in PAIRS:
            self.config = self.config.replace(pair, "")
        if self.config == prev_config:
            self.can_react = False


print("part1")
polymer = Polymer(TEST)
polymer.react()
assert polymer.config == "dabCBAcaDA"
assert len(polymer.config) == 10

with open("data/day05.txt") as f:
    lines = [line.strip() for line in f]
assert len(lines) == 1
INPUT = lines[0]
polymer = Polymer(INPUT)
polymer.react()
print(len(polymer.config))

print("part2")
lengths = []
for a, A in zip(string.ascii_lowercase, string.ascii_uppercase):
    INPUT_MOD = TEST.replace(a, "").replace(A, "")
    polymer = Polymer(INPUT_MOD)
    polymer.react()
    lengths.append(len(polymer.config))
assert min(lengths) == 4
lengths = []
for a, A in zip(string.ascii_lowercase, string.ascii_uppercase):
    INPUT_MOD = INPUT.replace(a, "").replace(A, "")
    polymer = Polymer(INPUT_MOD)
    polymer.react()
    lengths.append(len(polymer.config))
print(min(lengths))
