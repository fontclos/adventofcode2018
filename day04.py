import numpy as np
from typing import Iterator
from typing import List
"""
--- Day 4: Repose Record ---
You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)

--- Part Two ---
Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)

"""
TEST = [
    "[1518-11-02 00:50] wakes up",
    "[1518-11-01 00:25] wakes up",
    "[1518-11-01 00:55] wakes up",
    "[1518-11-03 00:29] wakes up",
    "[1518-11-04 00:46] wakes up",
    "[1518-11-05 00:55] wakes up",
    "[1518-11-03 00:05] Guard #10 begins shift",
    "[1518-11-01 23:58] Guard #99 begins shift",
    "[1518-11-05 00:03] Guard #99 begins shift",
    "[1518-11-04 00:02] Guard #99 begins shift",
    "[1518-11-01 00:00] Guard #10 begins shift",
    "[1518-11-02 00:40] falls asleep",
    "[1518-11-03 00:24] falls asleep",
    "[1518-11-01 00:30] falls asleep",
    "[1518-11-01 00:05] falls asleep",
    "[1518-11-04 00:36] falls asleep",
    "[1518-11-05 00:45] falls asleep"
]


class Shift:
    def __init__(self, year: str, month: str, day: str, guard: int) -> None:
        self.year = year
        self.month = month
        self.day = day
        self.guard = guard
        # initially the guard is never sleeping
        self.pattern = np.zeros(60)


class ShiftCollection:
    def __init__(self, shifts: List[Shift]) -> None:
        self.shifts = shifts
        self.guards = list(set([shift.guard for shift in shifts]))
        self._compute_total_minutes()

    def _compute_total_minutes(self):
        minutes = {guard: 0 for guard in self.guards}
        for shift in self.shifts:
            minutes[shift.guard] += np.sum(shift.pattern)
        self.total_minutes = minutes

    def get_guard_patterns(self, guard):
        pattern = [
            shift.pattern for shift in self.shifts if shift.guard == guard
        ]
        return pattern


def split_notes_by_shift(input: List[str]) -> Iterator[List[str]]:
    have_guard = [i for i, x in enumerate(
        sorted(input)) if x.find("Guard") > -1] + [len(input)]
    for i0, i1 in zip(have_guard[:-1], have_guard[1:]):
        yield sorted(input)[i0: i1]


def process_shift_notes(shift_notes: List[str]) -> Shift:
    head = shift_notes[0]
    tail = shift_notes[1:]
    # get the guard ID
    # text = Guard #10 begins shift
    _, text = head.strip("[").split("] ")
    _, guard, _, _ = text.split(" ")
    # get the date from the first tail element
    # tail[0] = "[1518-11-03 00:29] wakes up"
    if not tail:
        datetime, text = head.strip("[").split("] ")
        date, _ = datetime.split(" ")
        year, month, day = date.split("-")
        shift = Shift(year=year, month=month, day=day, guard=guard)
        pattern = np.zeros(60)
        shift.pattern = pattern
        return shift
    datetime, text = tail[0].strip("[").split("] ")
    date, _ = datetime.split(" ")
    year, month, day = date.split("-")
    shift = Shift(year=year, month=month, day=day, guard=guard)
    pattern = np.zeros(60)
    for ele in tail:
        datetime, text = ele.strip("[").split("] ")
        date, time = datetime.split(" ")
        hour, minute = time.split(":")
        year, month, day = date.split("-")
        assert year == shift.year
        assert month == shift.month
        assert day == shift.day
        if text == "falls asleep":
            pattern[int(minute):] = 1
        elif text == "wakes up":
            pattern[int(minute):] = 0
    shift.pattern = pattern
    return shift


def solve_part1(input: List[str], test=False):
    """
    Solve part 1 of day's 4 challenge

    Parameters
    ----------
    input : List[str]
        The puzzle's input
    test : bool, optional
        True if input is just the test input (the default is False)
    """

    shifts = []
    for shift_notes in split_notes_by_shift(input):
        shift = process_shift_notes(shift_notes)
        shifts.append(shift)
    shiftcollection = ShiftCollection(shifts=shifts)
    if test:
        assert shiftcollection.total_minutes == {'#10': 50.0, '#99': 30.0}
    total_mins, guards = np.array([[minutes, guard]
                                   for guard, minutes
                                   in shiftcollection.total_minutes.items()]).T
    maxmins = max(total_mins)
    # make sure the max is unique
    assert np.sum(total_mins == maxmins) == 1
    most_lazy = guards[np.argmax(total_mins)]
    if test:
        assert most_lazy == "#10"
    most_lazy_patterns = np.array(
        shiftcollection.get_guard_patterns(most_lazy))
    most_slept_minute = np.argmax(np.sum(most_lazy_patterns, axis=0))
    print(most_lazy, most_slept_minute)


def solve_part2(input: List[str], test=False):
    """
    Solve part 1 of day's 4 challenge

    Parameters
    ----------
    input : List[str]
        The puzzle's input
    test : bool, optional
        True if input is just the test input (the default is False)
    """

    shifts = []
    for shift_notes in split_notes_by_shift(input):
        shift = process_shift_notes(shift_notes)
        shifts.append(shift)
    shiftcollection = ShiftCollection(shifts=shifts)
    guards = []
    max_total_minutes = []
    most_sleeped_minutes = []
    for guard in shiftcollection.guards:
        arr = np.array(shiftcollection.get_guard_patterns(guard))
        total_minutes = np.sum(arr, axis=0)
        guards.append(guard)
        max_total_minutes.append(max(total_minutes))
        most_sleeped_minutes.append(np.argmax(total_minutes))

    chosen_guard = np.argmax(max_total_minutes)
    if test:
        assert guards[chosen_guard] == "#99"
        assert most_sleeped_minutes[chosen_guard] == 45
    print(guards[chosen_guard], most_sleeped_minutes[chosen_guard])


with open("data/day04.txt") as f:
    lines = [line.strip() for line in f]
solve_part1(TEST, test=True)
solve_part1(lines, test=False)
solve_part2(TEST, test=True)
solve_part2(lines, test=False)
