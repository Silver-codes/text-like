import random

from rich import box
from rich.console import Console
from rich.table import Table

from items import ITEMS_IN_LEVELS
from player import Player
from spells import SPELLS_IN_LEVELS
from upgrades import UPGRADES_IN_LEVELS
from weapons import WEAPONS_IN_LEVELS


def choose_cards(player, stage):
    available_cards = []
    level_num = stage[0]
    while level_num >= 1:
        level = f"level{level_num }"
        available_cards += ITEMS_IN_LEVELS[level] + SPELLS_IN_LEVELS[level] + WEAPONS_IN_LEVELS[level] + UPGRADES_IN_LEVELS[level]
        level_num -= 1
    random.shuffle(available_cards)
    card1, card2, card3 = (available_cards.pop() for _ in range(3))
    return card1, card2, card3


def card_roulette(player: Player, stage: list[int]): #TODO menu selection and application of cards.
    card1, card2, card3 = choose_cards(player, stage)
    console = Console()
    table = Table(title="Choose wisely", box= box.SIMPLE, safe_box=True, padding=(0,8), expand= True, title_justify="center")
    table.add_column(card1.name, justify="center", style=card1.card_color, header_style=card1.card_color)

    table.add_column(card2.name, justify="center", style=card2.card_color, header_style=card2.card_color)

    table.add_column(card3.name, justify="center", style=card3.card_color, header_style=card3.card_color)

    table.add_row(card1.description, card2.description, card3.description)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    from player import Player
    player = Player()
    stage = [1,1]
    card_roulette(player, stage)
