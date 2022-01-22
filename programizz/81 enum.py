from enum import Enum


class Day(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3


print(Day.Monday)
print(Day.Monday.value)
print(Day.Monday.name)
