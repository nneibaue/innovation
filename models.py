from pydantic import BaseModel, ConfigDict, RootModel
from enum import Enum, auto
from typing import List


class Effect(BaseModel):
    ...

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

# Icons belong on cards. Not sure if we need a backreference
class Icon(BaseModel):
    position: int
    symbol: Symbol

class Card(BaseModel):
    name: str
    age: int
    color: Color
    icons: List[Icon]
    effects: List[Effect]

# have methods of accessing cards based on conditions
class CardSet(RootModel):
    root: List[Card]

class BoardPile(BaseModel):
    cards: CardSet
    color: Color

class SupplyPile(BaseModel):
    cards: CardSet
    age: int

class Board(RootModel):
    root: List[BoardPile]

class Player(BaseModel):
    name: str
    board: BoardPile
    score: CardSet
    achievements: CardSet

class SpecialAchievement(BaseModel):
    ...

class Game(BaseModel):
    players: List[Player]
    supply: List[SupplyPile]
    available_achievements: CardSet
    special_achievements: List[SpecialAchievement]

