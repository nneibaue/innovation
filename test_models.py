import utils
import pytest
from pydantic import ValidationError

cards = utils.load_cards("cards")
from models import Symbol, CardSet, Color, BoardPile, SplayDirection


class TestCard:
    def test_filter_icons(self):
        card = cards.get("chemistry")
        icons = card.filter_icons([0, 2])
        assert [i.symbol for i in icons] == [Symbol.FACTORY, Symbol.FACTORY]

    def test_symbols(self):
        assert cards.get("astronomy").symbols == [
            Symbol.CROWN,
            Symbol.LIGHTBULB,
            Symbol.LIGHTBULB,
        ]


class TestCardSet:
    @pytest.fixture
    def sample(self):
        return CardSet(
            [
                cards.get("astronomy"),
                cards.get("reformation"),
                cards.get("perspective"),
                cards.get("medicine"),
                cards.get("paper"),
            ]
        )

    def test_getitem(self, sample):
        assert sample[0].name == "astronomy"

    def test_age(self, sample):
        assert sample.age(4).names == {"reformation", "perspective"}

    @pytest.mark.parametrize("c", ["purple", Color.PURPLE])
    def test_color(self, sample, c):
        assert sample.color(c).names == {"astronomy", "reformation"}

    def test_min_max_age(self, sample):
        assert sample.min_age == 3
        assert sample.max_age == 5

    def test_lowest_highest(self, sample):
        assert sample.lowest.names == {"medicine", "paper"}
        assert sample.highest.names == {"astronomy"}


class TestBoardPile:
    @pytest.fixture
    def red_pile(self):
        return BoardPile(
            [cards.get("optics"), cards.get("gunpowder"), cards.get("colonialism")]
        )

    def test_monochromaticity(self):
        # red cards
        _ = BoardPile([cards.get("gunpowder"), cards.get("coal")])

        # multicolor
        with pytest.raises(ValidationError):
            _ = BoardPile(
                [
                    cards.get("medicine"),  # yellow
                    cards.get("paper"),  # green
                ]
            )

    @pytest.mark.parametrize(
        "direction,expected",
        [
            (
                "left",
                [Symbol.FACTORY, Symbol.LIGHTBULB, Symbol.FACTORY, Symbol.FACTORY],
            ),
            (
                "right",
                [
                    Symbol.FACTORY,
                    Symbol.LIGHTBULB,
                    Symbol.FACTORY,
                    Symbol.FACTORY,
                    Symbol.CROWN,
                    Symbol.CROWN,
                ],
            ),
            (
                "up",
                [
                    Symbol.FACTORY,
                    Symbol.LIGHTBULB,
                    Symbol.FACTORY,
                    Symbol.FACTORY,
                    Symbol.CROWN,
                    Symbol.FACTORY,
                    Symbol.CROWN,
                    Symbol.CROWN,
                ],
            ),
        ],
    )
    def test_splay(self, red_pile, direction, expected):
        expected = sorted(expected, key=lambda s: s.value)
        found = sorted(red_pile.splay(direction).visible_symbols, key=lambda s: s.value)
        assert found == expected


    def test_meld(self, red_pile):
        red_pile.meld(cards.get('engineering'))
        assert red_pile.top.name == 'engineering'

        # can't meld other colors
        with pytest.raises(ValueError):
            red_pile.meld(
                cards.get('translation') # blue
            )

    def test_tuck(self, red_pile):
        red_pile.tuck(cards.get('engineering'))
        assert red_pile.bottom.name == 'engineering'

        # can't meld other colors
        with pytest.raises(ValueError):
            red_pile.tuck(
                cards.get('translation') # blue
            )


    def test_unsplay(self, red_pile):
        red_pile.splay('left').unsplay()
        assert len(red_pile.visible_icons) == 3
