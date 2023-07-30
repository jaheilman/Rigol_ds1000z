from enum import Enum, auto
from strenum import StrEnum, UppercaseStrEnum

# class Color(Enum):
#     RED = auto()
#     GREEN = auto()
#     BLUE = auto()

#     def __contains__(cls, item): 
#         try:
#             cls(item)
#         except ValueError:
#             return False
#         else:
#             return True
# def print_color(color:Color):
#     print(color)

# print("RED" in Color)
# print("PURPLE" in Color)

# print_color(Color.BLUE)
# print_color("RED")
# print_color("PURPLE")
# print_color(17)


class Example(UppercaseStrEnum):
    UPPER_CASE = auto()
    lower_case = auto()
    MixedCase = auto()

assert Example.UPPER_CASE == "UPPER_CASE"
assert Example.lower_case == "LOWER_CASE"
assert Example.MixedCase == "MIXEDCASE"