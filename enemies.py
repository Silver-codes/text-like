import random




class Enemy:
    def __init__(self) -> None:
        self.health = 100
        self.attack_power = 1
        self.mana = 40
        self.stamina = 50
        self.evasion = 0.0
        self.armor = 0

    def take_damage(self, damage_taken: float) -> bool:
        if self.evasion < random.random(): #checks if evades
            self.health -= round(damage_taken - self.armor)
            return True
        return False

    def attack(self, player):
        self.stamina -= 5
        return player.take_damage(self.attack_power)
