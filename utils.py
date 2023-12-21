from pydantic import TypeAdapter, validate_call, AfterValidator
from pathlib import Path
import yaml
import random
import jinja2 as j2

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


def create_card_enum(input_dir: str | Path):
    cards = load_cards(input_dir)
    cards.root.sort(key=lambda c: c.name.lower())
    with open('card_model.pytemplate', 'r') as f:
        template=j2.Template(f.read())

    with open('cards.py', 'w') as f:
        f.write(template.render(cards=cards, d=input_dir))
