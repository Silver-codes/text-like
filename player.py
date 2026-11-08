import random

from constants import (
    PLAYER_LOW_HEALTH_ADVANTAGE,
    PLAYER_LOW_HEALTH_THRESHOLD,
    PLAYER_STARTING_ARMOR,
    PLAYER_STARTING_ATTACK_POWER,
    PLAYER_STARTING_ATTACK_STAMINA_COST,
    PLAYER_STARTING_EVASION,
    PLAYER_STARTING_HEALTH,
    PLAYER_STARTING_MANA,
    PLAYER_STARTING_MANA_REGEN,
    PLAYER_STARTING_STAMINA,
    PLAYER_STARTING_STAMINA_REGEN,
)
from enemies import Enemy
from spells import FIREBALL, FROST_BEAM, Spell


class Player:
    def __init__(self) -> None:

        self.health = PLAYER_STARTING_HEALTH
        self.health_max = PLAYER_STARTING_HEALTH

        self.attack_power = PLAYER_STARTING_ATTACK_POWER
        self.attack_power_max = PLAYER_STARTING_ATTACK_POWER
        self.attack_stamina_cost = PLAYER_STARTING_ATTACK_STAMINA_COST

        self.stamina = PLAYER_STARTING_STAMINA
        self.stamina_max = PLAYER_STARTING_STAMINA
        self.stamina_regen = PLAYER_STARTING_STAMINA_REGEN

        self.spells: list[Spell] = [FIREBALL, FROST_BEAM]
        self.mana = PLAYER_STARTING_MANA
        self.mana_max = PLAYER_STARTING_MANA
        self.mana_regen = PLAYER_STARTING_MANA_REGEN

        self.evasion = PLAYER_STARTING_EVASION
        self.evasion_max = PLAYER_STARTING_EVASION

        self.armor = PLAYER_STARTING_ARMOR
        self.armor_max = PLAYER_STARTING_ARMOR

    @property
    def health_percentage(self) -> float:
        return (self.health / self.health_max) * 100

    def take_damage(self, damage_taken: float) -> int:
        if self.evasion < random.random(): #checks if evades
            if self.health_percentage > PLAYER_LOW_HEALTH_THRESHOLD: #recieves smaller damage when under x% health
                actual_damage = round(damage_taken - self.armor)
                self.health -= actual_damage
            else:
                actual_damage = round((damage_taken * PLAYER_LOW_HEALTH_ADVANTAGE) - self.armor)
                self.health -= actual_damage
            return actual_damage
        return 0

    def attack(self, enemy: Enemy) -> int: # TODO stamina handeling
        self.stamina -= self.attack_stamina_cost
        return enemy.take_damage(self.attack_power)

    def cast_spell(self, enemy, spell) -> int:  # TODO mana handeling
        self.mana -= spell.cost #acceses the mana cost (second position)
        return enemy.take_damage(spell.damage) #acceses the damage (first position)

    def regen(self):
        if self.stamina < self.stamina_max:
            self.stamina += self.stamina_regen
        if self.mana < self.mana_max:
            self.mana += self.mana_regen
