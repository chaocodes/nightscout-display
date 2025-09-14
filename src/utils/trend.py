from enum import Enum


class Trend(Enum):
    NONE = "NONE"
    FORTY_FIVE_UP = "FortyFiveUp"
    SINGLE_UP = "SingleUp"
    DOUBLE_UP = "DoubleUp"
    FORTY_FIVE_DOWN = "FortyFiveDown"
    SINGLE_DOWN = "SingleDown"
    DOUBLE_DOWN = "DoubleDown"
    FLAT = "Flat"
