import copy
import random
from posix import stat

from constants import (
    EFFECT_MESSAGES_ENEMY,
    EFFECT_TYPES,
    ENEMY_UNIT7_ARMOR,
    ENEMY_UNIT7_ATTACK_MESSAGES,
    ENEMY_UNIT7_ATTACK_POWER,
    ENEMY_UNIT7_EVASION,
    ENEMY_UNIT7_HEALTH,
    ENEMY_UNIT7_HEALTH_REGEN,
    ENEMY_UNIT7_MAGICK_POWER,
    ENEMY_UNIT7_STATE_EFFECTS,
    ENEMY_UNIT7_VULNERABILITY,
    ENEMY_VULNERABILITY,
)
from spells import ELECTRIC_PULSE, FIREBALL, FROST_BEAM, NO_SPELL, POISON_SPIKE


class Enemy:
    def __init__(self) -> None:
        self.name = "Test Enemy"
        self.health_max = 20
        self.__health = 20
        self.health_regen = 0
        self.attack_power = 3
        self.magic_power = 1
        self.mana = 40
        self.stamina = 50
        self.evasion = 0.0
        self.armor = 0
        self.vulnerability = ENEMY_VULNERABILITY
        self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES} # shows state effects - [dmg, num_rounds_left]
        self.attack_messages = [f"{self.name} attacks you for {damage} dmg"]

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

    def take_damage(self, damage_taken: float, spell):
        if self.evasion < random.random(): #checks if evades
            actual_damage = (damage_taken * self.vulnerability[spell.type]) - self.armor #calculates damage times vuln, minus armor
            actual_damage = round(actual_damage) # rounding, cause I want only integer hp
            actual_damage = max(actual_damage, 0) #actual dmg can't be negative
            self.health -= actual_damage

            #State effects
            state_effects = {} # creates a dict with no spell state effects
            effect_damage_adjusted = round(spell.effect_damage * self.vulnerability[spell.type])
            if spell.type in EFFECT_TYPES:
                state_effects[spell.type] = [effect_damage_adjusted, spell.effect_length]

            #Vulnerability message
            if self.vulnerability[spell.type] > 1:
                damage_info = "Critical hit!"
            elif self.vulnerability[spell.type] < 0.9:
                damage_info = "Not very effective..."
            else:
                damage_info = ""
            return actual_damage, damage_info, state_effects
        return 0, "Enemy evaded the attack", {}

    def attack(self, player):
        actual_damage = player.take_damage(self.attack_power, NO_SPELL)
        message = random.choice(self.attack_messages).format(damage=actual_damage)
        return actual_damage, message


    def cast_spell(self, player, spell) -> tuple[int, str]:
        spell_adjusted = copy.deepcopy(spell)
        spell_adjusted.damage *= self.magic_power
        spell_adjusted.damage = round(spell_adjusted.damage)
        spell_adjusted.effect_damage *= self.magic_power
        spell_adjusted.effect_damage = round(spell_adjusted.effect_damage)
        actual_damage = player.take_damage(spell_adjusted.damage, spell_adjusted)
        message = f"{self.name} casts {spell.name} dealing {actual_damage} dmg"
        return actual_damage, message


    def refresh(self): #actions that happen at the end of every round
        # Regeneration
        if self.health < self.health_max:
            self.health += self.health_regen

        # State effects (burn, poison)
        message = ""
        for effect, (damage, duration) in self.state_effects.items():
                if duration <= 0:
                    continue
                self.health -= damage
                message += EFFECT_MESSAGES_ENEMY[effect].format(name=self.name, damage=damage)
                self.state_effects[effect][1] -= 1
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

        self.magic_power = ENEMY_UNIT7_MAGICK_POWER
        self.spells: list[Spell] = [FIREBALL, FROST_BEAM, ELECTRIC_PULSE, POISON_SPIKE]

        self.evasion = ENEMY_UNIT7_EVASION

        self.armor = ENEMY_UNIT7_ARMOR

        self.vulnerability = ENEMY_UNIT7_VULNERABILITY

        self.state_effects = ENEMY_UNIT7_STATE_EFFECTS

        self.is_stunned = False

        self.attack_messages = ENEMY_UNIT7_ATTACK_MESSAGES

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
