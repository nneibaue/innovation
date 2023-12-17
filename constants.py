from enum import Enum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    PURPLE = auto()

class Symbol(Enum):
    CASTLE = auto()
    CROWN = auto()
    LEAF = auto()
    LIGHTBULB = auto()
    FACTORY = auto()
    CLOCK = auto()

class SplayDirection(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()