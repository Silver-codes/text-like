from math import remainder
import random
import time

from inquirer_textual import prompts
from inquirer_textual.common.Choice import Choice
from inquirer_textual.common.PromptSettings import PromptSettings
from inquirer_textual.InquirerApp import InquirerApp
from inquirer_textual.widgets.InquirerSelect import InquirerSelect
from rich.console import Console, Group
from rich.emoji import Emoji
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from clear_screen import clear_screen
from constants import CREEPY_MESSAGE_CHANCE, CREEPY_MESSAGES, EFFECT_EMOJIS, LOST_BATTLE_MESSAGES, WON_BATTLE_MESSAGES
from enemies import EnemyUnit7
from player import Player


#removing ? from menu
class NoQuestionApp(InquirerApp):
    CSS = "Prompt { display: none; }"


def select_menu(choices, settings=PromptSettings()):
    app = NoQuestionApp(theme=settings.theme)
    app.widget = InquirerSelect('', choices, mandatory=settings.mandatory)
    return app.run_with_settings(settings)

def generate_win_screen(enemy):
    content = Text(justify = "center")
    loss_message = random.choice(WON_BATTLE_MESSAGES).format(name=enemy.name)
    content.append(loss_message, style="bold green")
    table = Table.grid(expand=True)
    table.add_column(justify = "center")
    table.add_row()
    table.add_row(content)
    table.add_row()
    return table

def generate_loss_screen(enemy):
    content = Text(justify = "center")
    win_message = random.choice(LOST_BATTLE_MESSAGES).format(name=enemy.name)
    content.append(win_message, style="bold red")
    table = Table.grid(expand=True)
    table.add_column(justify = "center")
    table.add_row()
    table.add_row(content)
    table.add_row()
    return table

def check_for_win(player, enemy, console, turn_log):
    if enemy.health <= 0:
        creepy_message = ""
        console.clear()
        console.print(generate_game_screen(player, enemy, turn_log, creepy_message))
        console.print(generate_win_screen(enemy))
        time.sleep(5.0)
        return True
    return False

def check_for_loss(player, enemy, console, turn_log):
    if player.health <= 0:
        creepy_message = ""
        console.clear()
        console.print(generate_game_screen(player, enemy, turn_log, creepy_message))
        console.print(generate_loss_screen(enemy))
        time.sleep(5.0)
        return True
    return False

def state_emojis(unit):
    active = []
    for effect, (damage,duration) in unit.state_effects.items():
        if duration > 0:
            active.append(EFFECT_EMOJIS[effect])
    return " ".join(active)

def render_bar(current, maximum):
    length = 20
    blocks = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    total_steps = length * 8
    filled_steps = round((current / maximum) * total_steps)
    full_blocks = filled_steps // 8
    remaining_blocks = filled_steps % 8
    bar = "█" * full_blocks
    if full_blocks < length:
            bar += blocks[remaining_blocks]
            bar += " " * (length - full_blocks - 1)
    return f"|{bar}|"

def stat_line(label: str, current, maximum) -> str:
    current, maximum = round(current), round(maximum)
    numbers = f"{current}/{maximum}"
    return f"{label:>8}{render_bar(current, maximum)}{numbers:>8}\n" #change numbers max size from 7 to 9 if stats actually get over 999

def generate_game_screen(player, enemy, turn_log, creepy_message) -> Panel:
    #UI of the game screen
    content_player = Text(justify = "center")
    content_player.append(f"{player.name}\n", style="bold green")
    content_player.append(f"{Text.from_markup(state_emojis(player))}\n")
    content_player.append(stat_line("HP:", player.health, player.health_max),
                          style="red" if player.health > player.health_max * 0.25 else "bold red")
    content_player.append(stat_line("Stamina:", player.stamina, player.stamina_max), style="green")
    content_player.append(stat_line("Mana:", player.mana, player.mana_max), style="blue")

    action_text = Text(justify = "left")
    for message in turn_log:
            action_text.append(message + "\n")

    content_enemy = Text(justify = "center")
    content_enemy.append(f"{enemy.name}", style="bold red")
    content_enemy.append(f" | Revivals: {'N/A' if enemy.revivals is None else enemy.revivals}\n")
    content_enemy.append(f"{Text.from_markup(state_emojis(enemy))}\n")
    content_enemy.append(stat_line("HP:", enemy.health, enemy.health_max))


    ##TEMP##
    content_enemy.append(f"TEMP enemy Stamina: {enemy.stamina}/{enemy.stamina_max}\n")
    content_enemy.append(f"TEMP enemy Mana: {enemy.mana}/{enemy.mana_max}\n")
    ##TEMP##

    creepy_text = Text(justify = "right")
    creepy_text.append(creepy_message, style="italic red")

    table = Table.grid(expand=True)
    table.add_column(justify = "left", ratio=1)
    table.add_column(justify = "right", ratio=1)
    table.add_row(content_player, content_enemy)

    if creepy_text:
        layout = Group(table, action_text, creepy_text)
    else:
        layout = Group(table, action_text)

    return Panel(layout, title="[bold yellow]Stage placeholder (eg. 1st Floor)[/bold yellow]", border_style="blue")



# Game loop
def battle(player, enemy):
    console = Console()
    clear_screen()
    turn_log = []
    creepy_message = ""

    #Add back option to Cast Menu
    cast_menu = [Choice(f"{spell.name} ({spell.cost} mana)", data = spell) for spell in player.spells]
    if cast_menu == []:
        cast_menu.append(Choice("Back (You have no spells)", data = "back"))
    else:
        cast_menu.append(Choice("Back", data = "back"))

    # Main Battle lopp
    try:
        while True:
            console.clear()
            console.print(generate_game_screen(player, enemy, turn_log, creepy_message))

            if player.state_effects["stun"][1] > 0:
                turn_log = []
                turn_log.append("- You are stunned")
            else:
                #Menu
                result = select_menu([
                                    Choice(f"Attack ({player.attack_stamina_cost} stamina)", data="attack"),
                                    Choice('Cast', data="cast"),
                                    Choice('Defend', data="defend"),
                                    Choice('Forfeit', data="exit")],
                                        settings=PromptSettings(mandatory=False))

                #Player response and plain attack
                if result is None or result.value.data == "exit":
                    confirm = select_menu([
                                        Choice('Yes', data="yes"),
                                        Choice('No', data="no")],
                                            settings=PromptSettings(mandatory=False))
                    if confirm.value.data == "yes":
                        break
                    elif confirm.value.data == "no":
                        continue
                if result.value.data == "attack":
                    if player.stamina < player.attack_stamina_cost:
                        if "Not enough stamina" not in turn_log:
                            turn_log.append("Not enough stamina")
                        continue
                    turn_log = []
                    message = player.attack(enemy)
                    turn_log.append(f"- {message}")


                #Spell Casting
                elif result.value.data == "cast":
                    cast = select_menu(cast_menu,
                                            settings=PromptSettings(mandatory=False))
                    if cast.value.data == "back":
                        continue
                    spell = cast.value.data
                    if player.mana < spell.cost:
                        if "Not enough mana" not in turn_log:
                            turn_log.append("Not enough mana")
                        continue
                    turn_log = []
                    message = player.cast_spell(enemy, spell)
                    turn_log.append(f"- {message}")

                elif result.value.data == "defend":
                    turn_log = []
                    player.defend()
                    turn_log.append("- You prepare for an attack")

            creepy_message = ""
            #check for win condition
            if check_for_win(player, enemy, console, turn_log):
                return True

            console.clear()
            console.print(generate_game_screen(player, enemy, turn_log, creepy_message))

            if enemy.state_effects["stun"][1] > 0:
                turn_log.append(f"- {enemy.name} is stunned")
            else:
                enemy_message = enemy.take_turn(player) # TODO Enemy turn logic
                turn_log.append(f"- {enemy_message}")

                #check for loss condition
                if check_for_loss(player, enemy, console, turn_log):
                    return False


            time.sleep(1.5)
            console.clear()


            #refreshes and win/loss conditions
            player_refresh_message = player.refresh()
            enemy_refresh_message = enemy.refresh()
            if player_refresh_message != "":
                turn_log.append(f"{player_refresh_message}")
            if enemy_refresh_message != "":
                turn_log.append(f"{enemy_refresh_message}")


            if random.random() <= CREEPY_MESSAGE_CHANCE:
                creepy_message = random.choice(CREEPY_MESSAGES)

            console.print(generate_game_screen(player, enemy, turn_log, creepy_message))

            # Check for win/loss
            if check_for_win(player, enemy, console, turn_log):
                return True
            if check_for_loss(player, enemy, console, turn_log):
                return False


            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nGame exited.")


if __name__ == "__main__":
    from enemies import EnemyUnit7
    from player import Player
    player = Player()
    enemy = EnemyUnit7()
    enemy.intro_sequence()
    battle(player, enemy)
