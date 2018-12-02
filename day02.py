"""
--- Day 2: Inventory Management System ---
You stop falling through time, catch your breath, and check the screen on the device. "Destination reached. Current Year: 1518. Current Location: North Pole Utility Closet 83N10." You made it! Now, to find those anomalies.

Outside the utility closet, you hear footsteps and a voice. "...I'm not sure either. But now that so many people have chimneys, maybe he could sneak in that way?" Another voice responds, "Actually, we've been working on a new kind of suit that would let him fit through tight spaces like that. But, I heard that a few days ago, they lost the prototype fabric, the design plans, everything! Nobody on the team can even seem to remember important details of the project!"

"Wouldn't they have had enough fabric to fill several boxes in the warehouse? They'd be stored together, so the box IDs should be similar. Too bad it would take forever to search the warehouse for two similar box IDs..." They walk too far away to hear any more.

Late at night, you sneak to the warehouse - who knows what kinds of paradoxes you could cause if you were discovered - and use your fancy wrist device to quickly scan every box and produce a list of the likely candidates (your puzzle input).

To make sure you didn't miss any, you scan the likely candidate boxes again, counting the number that have an ID containing exactly two of any letter and then separately counting those with exactly three of any letter. You can multiply those two counts together to get a rudimentary checksum and compare it to what your device predicts.

For example, if you see the following box IDs:

abcdef contains no letters that appear exactly two or three times.
bababc contains two a and three b, so it counts for both.
abbcde contains two b, but no letter appears exactly three times.
abcccd contains three c, but no letter appears exactly two times.
aabcdd contains two a and two d, but it only counts once.
abcdee contains two e.
ababab contains three a and three b, but it only counts once.
Of these box IDs, four of them contain a letter which appears exactly twice, and three of them contain a letter which appears exactly three times. Multiplying these together produces a checksum of 4 * 3 = 12.

What is the checksum for your list of box IDs?

--- Part Two ---
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
"""
from collections import Counter
from itertools import combinations
from typing import List
import numpy as np

TEST1 = ["abcdef", "ababab", "abbcde", "abcccd", "aabcdd", "abcdee", "bababc"]
TEST2 = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]


def count_repetitions(word: str):
    counter = Counter(word)
    unique_counts = set(counter.values())
    pairs = 2 in unique_counts
    trios = 3 in unique_counts
    return [pairs, trios]


def checksum(word_list: List[str]) -> int:
    pairs_and_trios = [count_repetitions(word) for word in word_list]
    n_pairs, n_trios = np.sum(pairs_and_trios, axis=0)
    return n_pairs * n_trios


def compare_words(word1: str, word2: str):
    if sum([a != b for a, b in zip(word1, word2)]) == 1:
        return "".join([a for a, b in zip(word1, word2) if a == b])
    else:
        return None


def find_common_letters(word_list: List[str]) -> str:
    for word1, word2 in combinations(word_list, r=2):
        common = compare_words(word1, word2)
        if common is not None:
            break
    return common


assert count_repetitions("abcdef") == [False, False]
assert count_repetitions("bababc") == [True, True]
assert count_repetitions("abbcde") == [True, False]
assert count_repetitions("abcccd") == [False, True]
assert count_repetitions("aabcdd") == [True, False]
assert count_repetitions("abcdee") == [True, False]
assert count_repetitions("ababab") == [False, True]

assert checksum(TEST1) == 12
assert find_common_letters(TEST2) == "fgij"

part1 = np.loadtxt("data/day02_part1.txt", dtype=str)

print(checksum(part1))
print(find_common_letters(part1))
