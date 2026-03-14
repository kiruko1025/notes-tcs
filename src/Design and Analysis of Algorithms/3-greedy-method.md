# Greedy Method
Always make the choice that looks best at the moment.

## Earliest Ending Time
Given a set of activities with start and end times, select the maximum number of activities that don't overlap.
1. Sort activities by ending time.
2. Select the first activity.
3. For each subsequent activity, if its start time is greater than or equal to the ending time of the last selected activity, select it.