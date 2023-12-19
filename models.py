from pydantic import BaseModel, ConfigDict, RootModel, PrivateAttr, Field, model_validator, BeforeValidator, validate_call
from typing import List, Optional, Annotated, TypeVar
from collections import Counter

from constants import Color, Symbol, SplayDirection

T = TypeVar('T')

class CardNotFound(ValueError):
    ...

class DefaultModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

Upper = Annotated[T, BeforeValidator(str.upper)]
Lower = Annotated[T, BeforeValidator(str.lower)]

class DogmaEffect(DefaultModel):
    symbol: Upper[Symbol]
    demand: bool
    optional: bool
    text: str



# Icons belong on cards. Not sure if we need a backreference
class Icon(DefaultModel):
    position: int
    symbol: Upper[Symbol]


class Card(DefaultModel):
    name: Lower[str]
    age: int
    color: Upper[Color]
    icons: List[Icon]
    effects: List[DogmaEffect]

    @property
    def achievement_cost(self):
        return self.age * 5

    @property
    def symbols(self):
        return [icon.symbol for icon in self.icons]

    @property
    def filter_icons(self, positions: int | list[int]) -> List[Icon]:
        return [icon for icon in self.icons if icon.position in list(positions)]


# have methods of accessing cards based on conditions
class CardSet(RootModel):
    root: List[Card]

    def __getitem__(self, key):
        return self.root[key]

    def get(self, name: str) -> Card:
        for card in self.root:
            if card.name.lower() == name.lower():
                return card
        raise CardNotFound(name)


    def age(self, _age: int) -> "CardSet":
        return CardSet([c for c in self.root if c.age == _age])

    # validate_call doesn't work with forward refs
    def color(self, _color: str | Color) -> "CardSet":
        if isinstance(_color, str):
            _color = Color[_color.upper()]
        return CardSet([c for c in self.root if c.color == _color])

    @property
    def min_age(self) -> int:
        return min(self.root, key=lambda c: c.age)

    @property
    def max_age(self) -> int:
        return max(self.root, key=lambda c: c.age)


    def lowest(self) -> "CardSet":
        return [
            c for c in self.root if c.age == self.min_age
        ]

    def highest(self) -> "CardSet":
        return [
            c for c in self.root if c.age == self.min_age
        ]



class BoardPile(CardSet):
    '''Single color. Bottom card is index 0, top is -1'''

    _splay_direction: Optional[SplayDirection] = PrivateAttr(default=None)
    _color: Optional[Color] = PrivateAttr(default=None)
    
    @model_validator(mode='after')
    def set_color_and_assert_monochromaticity(self):
        if l := len(self.root) == 1:
            self._color = self.top.color
        elif l > 1:
            assert len({c.color for c in self.root}) == 1


    def meld(self, card: Card) -> None:
        self.root.append(card)

    def remove(self) -> Card:
        return self.root.pop(-1)

    def __len__(self):
        return len(self.root)

    @property
    def splayed(self) -> bool:
        return self._splay_direction is not None

    @property
    def splay_direction(self) -> SplayDirection:
        return self._splay_direction

    @property
    def top(self) -> Card:
        return self.root[-1]

    @property
    def visible_icons(self):
        icons = self.top.icons.copy()
        match self._splay_direction:
            case SplayDirection.LEFT:
                positions = [3]
            case SplayDirection.RIGHT:
                positions = [0, 1]
            case SplayDirection.UP:
                positions = [1, 2, 3]

        if self._splay_direction:
            for card in self.root[:1]:
                icons += card.filter_icons(positions)

        return icons

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
    def splayed(self) -> List[BoardPile]:
        return [pile for pile in self.root if pile._splay_direction]


    @property
    def splay_counts(self):
        directions = [p.splay_direction for p in self.splayed]
        return Counter(directions)


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



'''
splay, score, transfer, tuck, unsplay, reveal, return, meld
'''
class Player(DefaultModel):
    name: str
    board: BoardPile
    hand: CardSet
    score: CardSet
    achievements: CardSet






class SpecialAchievement(DefaultModel):
    ...


class Game(DefaultModel):
    players: List[Player]
    supply: List[SupplyPile]
    available_achievements: CardSet
    special_achievements: List[SpecialAchievement]

    _current_player: Player = PrivateAttr()
