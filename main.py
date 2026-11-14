import random

from battle import battle
from enemies import ALL_ENEMIES
from intro import intro_sequence
from main_menu import main_menu
from player import Player


def main():
    player = Player()
    main_menu()
    intro_sequence()
    for level in range(3):
        enemy = random.choice(ALL_ENEMIES)()
        if battle(player, enemy):
            enemy_class = type(enemy)
            if enemy_class.revivals is not None:
                enemy_class.revivals += 1





if __name__ == "__main__":
    main()
