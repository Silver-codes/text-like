from operator import truediv
import sys
import time
import random

sys.path.insert(0, "../")  # add main folder path to search list

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
from constants import EFFECT_EMOJIS, EFFECT_TYPES, LOST_BATTLE_MESSAGES, WON_BATTLE_MESSAGES
from enemies import Enemy_Unit7
from player import Player
from spells import FIREBALL, NO_SPELL, POISON_SPIKE, STUN

console = Console()

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

def check_for_win(enemy):
    if enemy.health <= 0:
        console.clear()
        console.print(generate_game_screen(player, enemy, turn_log))
        console.print(generate_win_screen(enemy))
        return True
    return False

def check_for_loss(player, enemy):
    if player.health <= 0:
        console.clear()
        console.print(generate_game_screen(player, enemy, turn_log))
        console.print(generate_loss_screen(enemy))
        return True
    return False

def state_emojis(unit):
    active = []
    for effect, (damage,duration) in unit.state_effects.items():
        if duration > 0:
            active.append(EFFECT_EMOJIS[effect])
    return " ".join(active)

player = Player()
enemy = Enemy_Unit7()
turn_log = []

def generate_game_screen(player, enemy, turn_log) -> Panel:
    #UI of the game screen
    content_player = Text(justify = "center")
    content_player.append("Player\n", style="bold green")
    content_player.append(f"Player HP: {player.health}/{player.health_max}\n", style="red" if player.health > player.health_max * 0.25 else "bold red")
    content_player.append(f"Player Stamina: {player.stamina}/{player.stamina_max}\n", style="green" if player.health > player.health_max * 0.25 else "bold red")
    content_player.append(f"Player Mana: {player.mana}/{player.mana_max}\n", style="blue" if player.health > player.health_max * 0.25 else "bold red")

    content_player.append(Text.from_markup(state_emojis(player)))

    action_text = Text(justify = "left")
    for message in turn_log:
            action_text.append(message + "\n")


    content_enemy = Text(justify = "center")
    content_enemy.append(f"{enemy.name}\n", style="bold red")
    content_enemy.append(f"Enemy HP: {enemy.health}/{enemy.health_max}\n")
    content_enemy.append(f"Revivals: {enemy.revivals}\n")

    ##TEMP##
    content_enemy.append(f"enemy Stamina: {enemy.stamina}/{enemy.stamina_max}\n")
    content_enemy.append(f"enemy Mana: {enemy.mana}/{enemy.mana_max}\n")
    ##TEMP##

    content_enemy.append(Text.from_markup(state_emojis(enemy)))

    table = Table.grid(expand=True)
    table.add_column(justify = "left", ratio=1)
    table.add_column(justify = "right", ratio=1)
    table.add_row(content_player, content_enemy)

    layout = Group(table, action_text)

    return Panel(layout, title="[bold yellow]Stage placeholder (eg. 1st Floor)[/bold yellow]", border_style="blue")



# Simulate a game loop
clear_screen()

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
        console.print(generate_game_screen(player, enemy, turn_log))

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
                    break
            if result.value.data == "attack":
                if player.stamina < player.attack_stamina_cost:
                    if "Not enough stamina" not in turn_log:
                        turn_log.append("Not enough stamina")
                    continue
                turn_log = []
                damage_dealt = player.attack(enemy)
                # Evasion handeling. Not the best, but works
                if "evaded" in damage_dealt[1]:
                    turn_log.append(f"- {damage_dealt[1]}")
                else:
                    turn_log.append(f"- You dealt {damage_dealt[0]} damage to enemy.")


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
                damage_dealt, damage_info, new_effects = player.cast_spell(enemy, spell)
                enemy.state_effects.update(new_effects)
                # Evasion handeling. Not the best, but works
                if "evaded" in damage_info:
                    turn_log.append(f"- {damage_info}")
                else:
                    turn_log.append(f"- You cast {spell.name} and deal {damage_dealt} damage to enemy. {damage_info}")

            elif result.value.data == "defend":
                turn_log = []
                player.defend()
                turn_log.append("- You prepare for an attack")


        #check for win condition
        if check_for_win(enemy):
            break

        console.clear()
        console.print(generate_game_screen(player, enemy, turn_log))

        if enemy.state_effects["stun"][1] > 0:
            turn_log.append(f"- {enemy.name} is stunned")
        else:
            enemy_message = enemy.take_turn(player) # TODO Enemy turn logic
            turn_log.append(f"- {enemy_message}")

            #check for loss condition
            if check_for_loss(player, enemy):
                break

        time.sleep(1.5)
        console.clear()


        #refreshes and win/loss conditions
        player_refresh_message = player.refresh()
        enemy_refresh_message = enemy.refresh()
        if player_refresh_message != "":
            turn_log.append(f"{player_refresh_message}")
        if enemy_refresh_message != "":
            turn_log.append(f"{enemy_refresh_message}")
        console.print(generate_game_screen(player, enemy, turn_log))

        # Check for win/loss
        if check_for_win(enemy):
            break
        if check_for_loss(player, enemy):
            break

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nGame exited.")
