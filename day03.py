"""
--- Day 3: No Matter How You Slice It ---
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
#123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:
A claim like

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

# 1 @ 1,3: 4x4
# 2 @ 3,1: 4x4
# 3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?

--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?

"""
from typing import NamedTuple, List
import numpy as np

TEST = ["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]


class claim(NamedTuple):
    cid: int
    left: int
    top: int
    width: int
    height: int
    right: int
    bottom: int


def get_canvas_size(claims):
    right = max([claim.right for claim in claims])
    bottom = max([claim.bottom for claim in claims])
    return right, bottom


def count_overclaimed(claims_str: List[str]) -> int:
    claims = process_claims(claims_str)
    max_width, max_height = get_canvas_size(claims)
    canvas = np.zeros((max_width, max_height))
    for claim in claims:
        canvas[claim.left: claim.right, claim.top: claim.bottom] += 1
    return ((canvas > 1).sum())


def process_claims(inputs: List[str]) -> List[claim]:
    """parse a list of claims

    Parameters
    ----------
    input : List[str]
        lines of input data

    Returns
    -------
    List[claim]
        A list of claim objects
    """
    claims = []
    for word in inputs:
        a, _, lt, wh = word.split(" ")
        lt = lt.strip(":")
        cid = a.strip("#")
        l, t = lt.split(",")
        w, h = wh.split("x")
        claims.append(claim(
            cid=int(cid),
            left=int(l),
            right=int(l) + int(w),
            top=int(t),
            bottom=int(t) + int(h),
            width=int(w),
            height=int(h),
        ))
    return claims


TEST = ["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]

assert count_overclaimed(TEST) == 4

with open("data/day03.txt") as f:
    part1 = [x.strip() for x in f]

# part 1
print(count_overclaimed(part1))

# part 2
claims = process_claims(part1)
max_width, max_height = get_canvas_size(claims)
canvas = np.zeros((max_width, max_height))
for claim in claims:
    canvas[claim.left: claim.right, claim.top: claim.bottom] += 1
for claim in claims:
    if set(canvas[claim.left: claim.right, claim.top: claim.bottom].reshape(-1)) == set([1]):
        print(claim.cid)
