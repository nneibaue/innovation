from pydantic import BaseModel, ConfigDict, RootModel, PrivateAttr, Field, model_validator
from typing import List, Optional
from collections import Counter

from constants import Color, Symbol, SplayDirection


class DefaultModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)


class Effect(DefaultModel):
    ...

    def enact(self):
        return "Enacting Effect"


# Icons belong on cards. Not sure if we need a backreference
class Icon(DefaultModel):
    position: int
    symbol: Symbol


class Card(DefaultModel):
    name: str
    age: int
    color: Color
    icons: List[Icon]
    effects: List[Effect]

    @property
    def achievement_cost(self):
        return self.age * 5


# have methods of accessing cards based on conditions
class CardSet(RootModel):
    root: List[Card]

    def age(self, _age: int) -> "CardSet":
        return CardSet([c for c in self.root if c.age == _age])

    def color(self, _color: Color) -> "CardSet":
        return CardSet([c for c in self.root if c.color == _color])


class BoardPile(DefaultModel):
    '''Single color. Bottom card is index 0, top is -1'''
    cards: CardSet = Field(default_factory=lambda: [])
    color: Color

    _splay_direction: Optional[SplayDirection] = PrivateAttr(default=None)

    @property
    def splayed(self) -> bool:
        return self._splay_direction is not None

    @property
    def splay_direction(self) -> SplayDirection:
        return self._splay_direction

    @property
    def top(self) -> Card:
        return self.cards[-1]

    @property
    def visible_icons(self):
        match self._splay_direction:
            case None:
                positions = [1, 2, 3]
            case SplayDirection.LEFT:
                positions = [3]
            case SplayDirection.RIGHT:
                positions = [0, 1]
            case SplayDirection.UP:
                positions = [1, 2, 3]
        cards = self.cards if self._splay_direction else [self.top]
        return [
            icon for card in cards for icon in card.icons if icon.position in positions
        ]

    @property
    def visible_symbols(self):
        return [icon.symbol for icon in self.visible_icons]

    @property
    def symbol_counts(self) -> int:
        return Counter(self.visible_symbols)

    def splay(self, direction: SplayDirection) -> None:
        self._splay_direction = direction

    def unsplay(self) -> None:
        self._splay_direction = None


class SupplyPile(DefaultModel):
    cards: CardSet
    age: int

    @property
    def empty(self):
        return not self.cards


class Board(RootModel):
    root: List[BoardPile]

    @model_validator(mode='after')
    def assert_one_pile_per_color(self):
        colors = [pile.color for pile in self.root]
        assert len(colors) == len(set(colors)), 'Boards can only have one pile per color'

    @property
    def symbol_counts(self):
        total = Counter()
        for pile in self.root:
            total += pile.symbol_counts
        return total

    @property
    def top_cards(self):
        return [pile.top for pile in self.root]

    def __getitem__(self, color: Color) -> BoardPile:
        '''Get piles by color reference'''
        for p in self.piles:
            if p.color == color:
                return p



class Player(DefaultModel):
    name: str
    board: BoardPile
    score: CardSet
    achievements: CardSet


class SpecialAchievement(DefaultModel):
    ...


class Game(DefaultModel):
    players: List[Player]
    supply: List[SupplyPile]
    available_achievements: CardSet
    special_achievements: List[SpecialAchievement]
