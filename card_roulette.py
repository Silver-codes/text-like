import random
import time

from inquirer_textual.common.Choice import Choice
from inquirer_textual.common.PromptSettings import PromptSettings
from inquirer_textual.InquirerApp import InquirerApp
from inquirer_textual.widgets.InquirerSelect import InquirerSelect
from rich import box
from rich.console import Console
from rich.table import Table

from clear_screen import clear_screen
from items import ITEMS_IN_LEVELS
from player import Player
from spells import SPELLS_IN_LEVELS
from upgrades import UPGRADES_IN_LEVELS
from weapons import WEAPONS_IN_LEVELS


#removing ? from menu
class NoQuestionApp(InquirerApp):
    CSS = "Prompt { display: none; }"


def select_menu(choices, settings=PromptSettings()):
    app = NoQuestionApp(theme=settings.theme)
    app.widget = InquirerSelect('', choices, mandatory=settings.mandatory)
    return app.run_with_settings(settings)


def choose_cards(player, stage):
    available_cards = []
    level_num = stage[0]
    while level_num >= 1:
        level = f"level{level_num }"
        available_cards += ITEMS_IN_LEVELS[level] + SPELLS_IN_LEVELS[level] + WEAPONS_IN_LEVELS[level] + UPGRADES_IN_LEVELS[level]
        level_num -= 1
    held_cards = [player.weapon] + player.spells
    available_cards = [card for card in available_cards if card not in held_cards]
    random.shuffle(available_cards)
    card1, card2, card3 = (available_cards.pop() for _ in range(3))
    return card1, card2, card3


def card_roulette(player: Player, stage: list[int]):

    card1, card2, card3 = choose_cards(player, stage)

    while True:
        clear_screen()
        console = Console()
        table = Table(title="Choose wisely", box= None, safe_box=True, padding=(0,8), expand= True, title_justify="center")
        table.add_column(justify="center", style=card1.card_color, header_style=card1.card_color, ratio=1)

        table.add_column(justify="center", style=card2.card_color, header_style=card2.card_color, ratio=1)

        table.add_column(justify="center", style=card3.card_color, header_style=card3.card_color, ratio=1)
        table.add_row(card1.name, card2.name, card3.name, style="bold")
        table.add_row(card1.card_type, card2.card_type, card3.card_type)
        table.add_row()
        table.add_row(card1.description, card2.description, card3.description)

        console.print(table)
        print()


        result = select_menu([
                            Choice(card1.name, data="card1"),
                            Choice(card2.name, data="card2"),
                            Choice(card3.name, data="card3"),
                            Choice("I don't want any", data="exit")],
                                settings=PromptSettings(mandatory=False))

        #Exit
        if result is None or result.value.data == "exit":
            confirm = select_menu([
                                Choice('Yes', data="yes"),
                                Choice('No', data="no")],
                                    settings=PromptSettings(mandatory=False))
            if confirm.value.data == "yes":
                break
            elif confirm.value.data == "no":
                continue


        #Card selection
        if result.value.data == "card1":
            console.print(card1.pick_up(player), style=f"bold {card1.card_color}")
            # print(player.weapon.name)
            # print(f"Health:{player.health}")
            # print(f"stamina:{player.stamina}")
            # print(f"mana:{player.mana}")
            # print(f"evasion:{player.evasion}")
            # print(f"armor:{player.armor}")
            # print([spell.name for spell in player.spells])
            # print([upgrade.name for upgrade in player.upgrades])
            # print(", ".join(f"{item.name} x{count}" for item, count in player.items.items()))
            print()
            input(">> PRESS [ENTER] TO CONTINUE <<")
            break

        if result.value.data == "card2":
            console.print(card2.pick_up(player), style=f"bold {card2.card_color}")
            print()
            input(">> PRESS [ENTER] TO CONTINUE <<")
            break

        if result.value.data == "card3":
            console.print(card3.pick_up(player), style=f"bold {card3.card_color}")
            print()
            input(">> PRESS [ENTER] TO CONTINUE <<")
            break


if __name__ == "__main__":
    from player import Player
    player = Player()
    stage = [1,1]
    card_roulette(player, stage)
