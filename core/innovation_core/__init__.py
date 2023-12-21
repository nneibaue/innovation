import logging
from importlib.resources import files


PROJECT_ROOT = files('innovation_core')

from .models import (
    CardSet,
    BoardPile,
    Board,
    Player,
    Game,
    Icon,
    SupplyPile,
    Card,
    DogmaEffect
)

from .constants import (
    Color,
    Symbol,
    SplayDirection
)

from pathlib import Path
from pydantic import TypeAdapter
from typing import List
import random
import yaml

def _load_cards(d: str | Path, shuffle: bool = True) -> CardSet:
    d = Path(d)
    adapter = TypeAdapter(List[Card])
    cards = []
    for f in d.glob('*.yaml'):
        with open(f, 'r') as cardfile:
           new_cards = adapter.validate_python(
               yaml.safe_load(cardfile.read())
           ) 
           cards += new_cards
    if not cards:
        raise ValueError(f'No valid card_data found in {d}')
    return CardSet(cards)

ALL_CARDS = _load_cards(PROJECT_ROOT / 'card_data')

try:
    from .cards import Cards
except Exception:
    logging.warning('Cards module could not be imported. This is expected when running `synthesize`.')
