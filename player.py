import copy
import random
from math import log

from constants import (
    EFFECT_MESSAGES_PLAYER,
    EFFECT_TYPES,
    PLAYER_ATTACK_MESSAGES,
    PLAYER_LOW_HEALTH_ADVANTAGE,
    PLAYER_LOW_HEALTH_THRESHOLD,
    PLAYER_STARTING_ARMOR,
    PLAYER_STARTING_ATTACK_POWER,
    PLAYER_STARTING_ATTACK_STAMINA_COST,
    PLAYER_STARTING_DEFEND_ARMOR,
    PLAYER_STARTING_DEFEND_ARMOR_DURATION,
    PLAYER_STARTING_EVASION,
    PLAYER_STARTING_HEALTH,
    PLAYER_STARTING_MAGICK_POWER,
    PLAYER_STARTING_MANA,
    PLAYER_STARTING_MANA_REGEN,
    PLAYER_STARTING_STAMINA,
    PLAYER_STARTING_STAMINA_REGEN,
    PLAYER_STARTING_VULNERABILITY,
)
from enemies import Enemy
from spells import (
    ELECTRIC_PULSE,
    FIREBALL,
    FROST_BEAM,
    POISON_SPIKE,
    SPELL_CAST_MESSAGES_PLAYER,
    STUN,
    Spell,
)


class Player:
    def __init__(self) -> None:

        self.__health = PLAYER_STARTING_HEALTH
        self.health_max = PLAYER_STARTING_HEALTH

        self.attack_power = PLAYER_STARTING_ATTACK_POWER
        self.attack_power_max = PLAYER_STARTING_ATTACK_POWER
        self.attack_stamina_cost = PLAYER_STARTING_ATTACK_STAMINA_COST

        self.__stamina = PLAYER_STARTING_STAMINA
        self.stamina_max = PLAYER_STARTING_STAMINA
        self.stamina_regen = PLAYER_STARTING_STAMINA_REGEN

        self.magic_power = PLAYER_STARTING_MAGICK_POWER
        self.spells: list[Spell] = [FIREBALL, FROST_BEAM, ELECTRIC_PULSE, POISON_SPIKE, STUN]
        self.__mana = PLAYER_STARTING_MANA
        self.mana_max = PLAYER_STARTING_MANA
        self.mana_regen = PLAYER_STARTING_MANA_REGEN

        self.evasion = PLAYER_STARTING_EVASION
        self.evasion_max = PLAYER_STARTING_EVASION

        self.armor = PLAYER_STARTING_ARMOR
        self.armor_max = PLAYER_STARTING_ARMOR
        self.defend_armor = PLAYER_STARTING_DEFEND_ARMOR
        self.defend_armor_active = 0
        self.defend_armor_duration = PLAYER_STARTING_DEFEND_ARMOR_DURATION

        self.vulnerability = PLAYER_STARTING_VULNERABILITY

        self.state_effects = self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES} # shows state effects - [dmg, num_rounds_left]
        # for defend its [0, num_rounds left], dmg reduced by defend set in self.defend_armor


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

    @property
    def health_percentage(self) -> float:
        if self.health_max <= 0:
            return 0.0
        return (self.health / self.health_max) * 100

    @property
    def stamina(self):
        return self.__stamina

    @stamina.setter
    def stamina(self, value):
        if value < 0:
            self.__stamina = 0
        elif value > self.stamina_max:
            self.__stamina = self.stamina_max
        else:
            self.__stamina = value

    @property
    def mana(self):
        return self.__mana

    @mana.setter
    def mana(self, value):
        if value < 0:
            self.__mana = 0
        elif value > self.mana_max:
            self.__mana = self.mana_max
        else:
            self.__mana = value

    def take_damage(self, damage_taken: float):
        if self.health_percentage > PLAYER_LOW_HEALTH_THRESHOLD: #recieves smaller damage when under x% health
            actual_damage = round(damage_taken - (self.armor + self.defend_armor_active))
            actual_damage = max(actual_damage, 0) #actual dmg can't be negative
            self.health -= actual_damage
        else:
            actual_damage = round((damage_taken * PLAYER_LOW_HEALTH_ADVANTAGE) - (self.armor + self.defend_armor_active))
            actual_damage = max(actual_damage, 0) #actual dmg can't be negative
            self.health -= actual_damage
        return actual_damage


    def attack(self, enemy: Enemy):
        self.stamina -= self.attack_stamina_cost

        #Evasion check
        if self.enemy_evades(enemy):
            message = random.choice(enemy.evade_messages)
            return message

        actual_damage = enemy.take_damage(self.attack_power)
        message = random.choice(PLAYER_ATTACK_MESSAGES).format(enemy=enemy.name, damage=actual_damage)
        return message

    def cast_spell(self, enemy, spell) -> str:
        self.mana -= spell.cost #acceses the mana cost

        #Evasion check
        if self.enemy_evades(enemy):
            message = random.choice(enemy.evade_messages)
            return message

        spell_adjusted = copy.deepcopy(spell)
        spell_adjusted.damage *= self.magic_power
        spell_adjusted.damage = round(spell_adjusted.damage)
        spell_adjusted.effect_damage *= self.magic_power
        spell_adjusted.effect_damage = round(spell_adjusted.effect_damage)
        actual_damage = enemy.take_damage(spell_adjusted.damage)
        message = random.choice(SPELL_CAST_MESSAGES_PLAYER[spell]).format(enemy=enemy.name, damage=actual_damage)

        #State effects
        state_effects = {} # creates a dict with no spell state effects
        effect_damage_adjusted = round(spell.effect_damage * enemy.vulnerability[spell.type])
        if spell.type in EFFECT_TYPES:
            state_effects[spell.type] = [effect_damage_adjusted, spell.effect_length]
        enemy.state_effects.update(state_effects) #.update on empty list does nothing, so it's safe to use

        #Vulnerability message
        if self.vulnerability[spell.type] > 1:
            message += " Critical hit!"
        elif self.vulnerability[spell.type] < 0.9:
            message += " Not very effective..."
        else:
            message += ""

        return message

    def defend(self):
        self.defend_armor_active = self.defend_armor
        self.state_effects["defend"] = [0, self.defend_armor_duration]

    def enemy_evades(self, enemy) -> bool:
        return random.random() < enemy.evasion

    def refresh(self): #actions that happen at the end of every round
        # Regeneration
        if self.stamina < self.stamina_max:
            self.stamina += self.stamina_regen
        if self.mana < self.mana_max:
            self.mana += self.mana_regen

        # State effects (burn, poison)
        message = ""
        for effect, (damage, duration) in self.state_effects.items():
                if duration <= 0:
                    continue
                self.health -= damage
                if effect in EFFECT_MESSAGES_PLAYER:
                    message += EFFECT_MESSAGES_PLAYER[effect].format(damage=damage)
                self.state_effects[effect][1] -= 1
        if self.state_effects["defend"] == [0, 0]:
            self.defend_armor_active = 0
        return message
