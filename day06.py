from typing import List
from scipy.spatial import distance_matrix
import pandas as pd
import numpy as np

"""--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

"""


def solve_part1(input: List[str]) -> int:
    """
    Solve part 1. This is the wrong way to do it but I'm tired.

    Parameters
    ----------
    input : List[str]
        Puzzle input as list of strings (lines)

    Returns
    -------
    int
        Size of the maximum non-infinite area
    """
    # make a dataframe for the center of all zones
    data = []
    for zone_idx, line in enumerate(input):
        x, y = line.split(", ")
        x = int(x)
        y = int(y)
        data.append([zone_idx, x, y])

    zones = pd.DataFrame(
        data=data,
        columns=["zone_id", "x", "y"]
    ).set_index("zone_id")

    # make a dataframe for all points in the grid
    data = []
    xmin, xmax = zones.x.min(), zones.x.max()
    ymin, ymax = zones.y.min(), zones.y.max()
    pcount = -1
    for x in range(xmax+2):
        for y in range(ymax+2):
            pcount += 1
            data.append([pcount, x, y])
    points = pd.DataFrame(
        data=data,
        columns=["point_id", "x", "y"]
    ).set_index("point_id")

    # compute all-to-all distances
    D = distance_matrix(zones, points, p=1)
    distances = pd.DataFrame(
        data=D,
        index=zones.index,
        columns=points.index
    ).T

    # which zone is closest to each point
    point_closest = distances.idxmin(axis=1)

    # deal with ties wich we have not detected
    non_unique_min = ((distances.T == distances.min(axis=1)).T).sum(axis=1) > 1
    point_closest.loc[non_unique_min] = np.nan

    # put them in a grid
    grid = np.zeros((xmax+2, ymax+2))*np.nan
    for pid in points.index:
        x, y = points.loc[pid]
        grid[x, y] = point_closest.loc[pid]

    # deal with borders
    top = list(grid[:, 0])
    bottom = list(grid[:, -1])
    left = list(grid[0, :])
    right = list(grid[-1, :])
    touch_the_border = set(top + bottom + left + right)

    # count areas
    areas = point_closest.value_counts()
    valid_areas = [area
                   for idx, area in dict(areas).items()
                   if idx not in touch_the_border
                   ]
    return max(valid_areas)


def solve_part2(input, threshold):
    """I was lucky and could solve part 2 very easily with my setup..."""
    data = []
    for zone_idx, line in enumerate(input):
        x, y = line.split(", ")
        x = int(x)
        y = int(y)
        data.append([zone_idx, x, y])

    zones = pd.DataFrame(
        data=data,
        columns=["zone_id", "x", "y"]
    ).set_index("zone_id")

    # make a dataframe for all points in the grid
    data = []
    xmin, xmax = zones.x.min(), zones.x.max()
    ymin, ymax = zones.y.min(), zones.y.max()
    pcount = -1
    for x in range(xmax+2):
        for y in range(ymax+2):
            pcount += 1
            data.append([pcount, x, y])
    points = pd.DataFrame(
        data=data,
        columns=["point_id", "x", "y"]
    ).set_index("point_id")

    # compute all-to-all distances
    D = distance_matrix(zones, points, p=1)
    distances = pd.DataFrame(
        data=D,
        index=zones.index,
        columns=points.index
    ).T

    total_distances = distances.sum(axis=1)
    return (total_distances < threshold).sum()


TEST = [
    "1, 1",
    "1, 6",
    "8, 3",
    "3, 4",
    "5, 5",
    "8, 9"
]

print("test case:")
print("part 1:", solve_part1(TEST))
print("part 2:", solve_part2(TEST, 32))
print()

with open("data/day06.txt") as f:
    REAL = [line.strip() for line in f]

print("real case:")
print("part 1:", solve_part1(REAL))
print("part 2:", solve_part2(REAL, 10_000))
