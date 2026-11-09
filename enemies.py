import random

from constants import (
    ENEMY_UNIT7_ARMOR,
    ENEMY_UNIT7_ATTACK_POWER,
    ENEMY_UNIT7_EVASION,
    ENEMY_UNIT7_HEALTH,
    ENEMY_UNIT7_HEALTH_REGEN,
    ENEMY_UNIT7_STATE_FIRE,
    ENEMY_UNIT7_STATE_POISON,
    ENEMY_UNIT7_VULNERABILITY,
    ENEMY_VULNERABILITY)



class Enemy:
    def __init__(self) -> None:
        self.name = "Test Enemy"
        self.health_max = 20
        self.__health = 20
        self.health_regen = 0
        self.attack_power = 3
        self.mana = 40
        self.stamina = 50
        self.evasion = 0.0
        self.armor = 0
        self.vulneribility = ENEMY_VULNERABILITY
        self.state_fire = [5, 1] # shows if entity is burning - [dmg, num_rounds_left]
        self.state_poison = [6, 3] # shows if entity is poisoned - [dmg, num_rounds_left]

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

    def take_damage(self, damage_taken: float, type: str) -> tuple[int, str]:
        if self.evasion < random.random(): #checks if evades
            actual_damage = (damage_taken * self.vulneribility[type]) - self.armor
            actual_damage = round(actual_damage) # rounding, cause I want only integer hp
            actual_damage = max(actual_damage, 0) #actual dmg can't be negative
            self.health -= actual_damage
            if self.vulneribility[type] > 1:
                damage_info = "Critical hit!"
            elif self.vulneribility[type] < 0.9:
                damage_info = "Not very effective..."
            else:
                damage_info = ""
            return actual_damage, damage_info
        return 0, "Enemy evaded the attack"

    def attack(self, player):
        return player.take_damage(self.attack_power, "normal")

    def refresh(self): #actions that happen at the end of every round
        # Regeneration
        if self.health < self.health_max:
            self.health += self.health_regen

        # State effects (burn, poison)
        message = ""
        if self.state_fire[1] > 0:
            self.health -= self.state_fire[0]
            self.state_fire[1] -= 1
            message += f"{self.name} burn for {self.state_fire[0]} dmg. "
        if self.state_poison[1] > 0:
            self.health -= self.state_poison[0]
            self.state_poison[1] -= 1
            message += f"{self.name} is poisoned for {self.state_fire[0]} dmg"
        return message

#1 Unit 7-Null
class Enemy_Unit7(Enemy):
    def __init__(self):
        self.name = "Unit 7-Null"
        self.revivals = "N/A"

        self.health_max = ENEMY_UNIT7_HEALTH
        self.__health = ENEMY_UNIT7_HEALTH
        self.health_regen = ENEMY_UNIT7_HEALTH_REGEN

        self.attack_power = ENEMY_UNIT7_ATTACK_POWER

        self.evasion = ENEMY_UNIT7_EVASION

        self.armor = ENEMY_UNIT7_ARMOR

        self.vulneribility = ENEMY_UNIT7_VULNERABILITY

        self.state_fire = ENEMY_UNIT7_STATE_FIRE # shows if entity is burning - [dmg, num_rounds_left]
        self.state_poison = ENEMY_UNIT7_STATE_POISON # shows if entity is poisoned - [dmg, num_rounds_left]

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
