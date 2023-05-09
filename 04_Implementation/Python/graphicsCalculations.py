"""
Class providing an algorythm to calculate attention over time for the final statistic
"""


LIMIT_CONST = 3
FACTOR_CONST = 10
TO_MINUTES = 60000000


def linegraph_creator(starttime: int, endtime: int, zone_events: list) -> list:
    """
    Method that creates an array that contains data for a linegraph, takes an array of event times and a duration value

    IMPORTANT:
    - Eventtimes are zone_stats:
        - minimum 0 (first 60s of the meeting)
        - maximum "duration" (very end of meeting)

    Parameters
    ----------
    starttime : int
        Timestamp when recording started. Must be a UNIX timestamp.
    endtime : int
        Timestamp when recording ended. Must be a UNIX timestamp.
    zone_events : list
        List of all events that occured. For more details see processing.py.

    Returns
    -------
    An (array) list holding the attention level for each minute of the recorded data
    """
    duration = ((int(endtime) - int(starttime)) + TO_MINUTES - 1) // TO_MINUTES
    minutes = [100] * duration

    eventtimes = []
    for event in zone_events:
        if event[4] == True:
            relativeTime = (int(event[1]) - int(starttime)) // TO_MINUTES
            eventtimes.append(relativeTime)
    for e in eventtimes:
        for i in range(len(minutes)):
            # "right" of the event
            if (i < (e + LIMIT_CONST)) and (i >= e):
                deduction = (LIMIT_CONST + (e-i)) * FACTOR_CONST
                minutes[i] = minutes[i] - deduction
            # "left" side of event
            if (i > (e - LIMIT_CONST)) and (i < e):
                deduction = (LIMIT_CONST - (e-i)) * FACTOR_CONST
                minutes[i] = minutes[i] - deduction

    # ensures that there are no negative attention values (sets everything negative to 0)
    for m in range(len(minutes)):
        if minutes[m] < 0:
            minutes[m] = 0
    return minutes
