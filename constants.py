from enum import Enum, auto

class Color(Enum):
    RED = 'RED'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    YELLOW = 'YELLOW'
    PURPLE = 'PURPLE'

class Symbol(Enum):
    CASTLE = 'CASTLE'
    CROWN = 'CROWN'
    LEAF = 'LEAF'
    LIGHTBULB = 'LIGHTBULB'
    FACTORY = 'FACTORY'
    CLOCK = 'CLOCK'

class SplayDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'

