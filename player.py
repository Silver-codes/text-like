import random

from enemies import Enemy


class Player:
    def __init__(self) -> None:
        self.health_max = 100
        self.health = 100
        self.attack_power = 3
        self.mana = 40
        self.stamina = 50
        self.evasion = 0.0
        self.armor = 0

    @property
    def health_percentage(self) -> float:
        return (self.health / self.health_max) * 100

    def take_damage(self, damage_taken: float) -> bool:
        if self.evasion < random.random(): #checks if evades
            if self.health_percentage > 20: #recieves smaller damage when under 20% health
                self.health -= round(damage_taken - self.armor)
            else:
                self.health -= round((damage_taken * 0.66) - self.armor)
            return True
        return False

    def attack(self, enemy: Enemy) ->bool:
        self.stamina -= 5
        return enemy.take_damage(self.attack_power)
