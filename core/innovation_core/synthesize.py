import jinja2 as j2
import fire

from . import PROJECT_ROOT, ALL_CARDS
TEMPLATE = PROJECT_ROOT / 'card_model.py.j2'

def synthesize_card_enum(input_dir: str = 'card_data', output_file: str = 'cards.py') -> None:
    ALL_CARDS.root.sort(key=lambda c: c.name.lower())
    with open(TEMPLATE, 'r') as f:
        template=j2.Template(f.read())

    with open(PROJECT_ROOT / output_file, 'w') as f:
        f.write(template.render(cards=ALL_CARDS))

if __name__ == '__main__':
    fire.Fire(synthesize_card_enum)