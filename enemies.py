import random


class Enemy:
    def __init__(self) -> None:
        self.health_max = 20
        self.__health = 20
        self.attack_power = 3
        self.mana = 40
        self.stamina = 50
        self.evasion = 0.0
        self.armor = 0

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        elif value > self.health_max:
            self.__health = self.health_max
        else:
            self.__health = value

    def take_damage(self, damage_taken: float) -> int:
        if self.evasion < random.random(): #checks if evades
            actual_damage = round(damage_taken - self.armor)
            actual_damage = max(actual_damage, 0) #actual dmg can't be negative
            self.health -= actual_damage
            return actual_damage
        return 0

    def attack(self, player):
        self.stamina -= 5
        return player.take_damage(self.attack_power)
