import utils
import pytest

cards = utils.load_cards("cards")
from models import Symbol, CardSet, Color


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
        assert sample[0].name == 'astronomy'

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
