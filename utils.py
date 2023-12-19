from pydantic import TypeAdapter, validate_call, AfterValidator
from pathlib import Path
import yaml
import random

from models import CardSet, Card
from typing import Annotated, List


def load_cards(d: str | Path, shuffle: bool = True) -> CardSet:
    d = Path(d)
    adapter = TypeAdapter(List[Card])
    cards = []
    for f in d.glob('*.yaml'):
        with open(f, 'r') as cardfile:
           new_cards = adapter.validate_python(
               yaml.safe_load(cardfile.read())
           ) 
           cards += new_cards
    if shuffle:
        random.shuffle(cards)
    return CardSet(cards)