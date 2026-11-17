import random

from battle import battle
from enemies import ALL_ENEMIES
from intro import intro_sequence
from main_menu import main_menu
from player import Player


def main():
    player = Player()
    main_menu()
    #intro_sequence()
    for level in range(3):
        for sublevel in range(5):
            enemy = random.choice(ALL_ENEMIES)()
            stage = [level + 1, sublevel + 1] #count starts from 0, therefore + 1
            if battle(player, enemy, stage):
                enemy.on_defeated()





if __name__ == "__main__":
    main()
