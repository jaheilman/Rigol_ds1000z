from enum import Enum, auto
from strenum import StrEnum

class MeasureSource(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    OFF = auto()
    D0 = auto()
    D1 = auto()
    D2 = auto()
    D3 = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    D7 = auto()
    D8 = auto()
    D9 = auto()
    D10 = auto()
    D11 = auto()
    D12 = auto()
    D13 = auto()
    D14 = auto()
    D15 = auto()

class AnalogChannels(StrEnum):
    CHAN1 = auto()
    CHAN2 = auto()
    CHAN3 = auto()
    CHAN4 = auto()
    MATH = auto()


def MeasureItems(StrEnum):
    ITEM1 = auto()
    ITEM2 = auto()
    ITEM3 = auto()
    ITEM4 = auto()
    ITEM5 = auto()
    ALL = auto()

def MeasureStatisticsDisplay(StrEnum):
    difference = auto()
    extremum = auto()
    DIFF = auto()
    EXTR = auto()