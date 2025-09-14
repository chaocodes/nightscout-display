from enum import Enum


class Status(Enum):
    LOW = 0
    LOW_CRITICAL = 1
    HIGH = 2
    HIGH_CRITICAL = 3
    OK = 4
