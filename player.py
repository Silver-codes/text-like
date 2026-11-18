import copy
import random

from constants import (
    EFFECT_MESSAGES_PLAYER,
    EFFECT_TYPES,
    PLAYER_LOW_HEALTH_ADVANTAGE,
    PLAYER_LOW_HEALTH_THRESHOLD,
)
from enemies import Enemy
from items.restore_items import HEALTH_SYRINGE, MANA_NANOBOTS, STAMINA_CARTRIDGE
from spells import (
    ELECTRIC_PULSE,
    FIREBALL,
    FROST_BEAM,
    POISON_DART,
    POISON_SPIKE,
    SEMPRA_SECTUM,
    SPARK,
    SPELL_CAST_MESSAGES_PLAYER,
    STUN,
    TELEKINESIS,
    Spell,
)
from weapons import FISTS, WEAPON_ATTACK_MESSAGES


class Player:
    def __init__(self) -> None:
        self.name = "Player"

        self.__health = 50
        self.health_max = 50

        self.weapon = FISTS
        self.strength = 1 # is multiplied by
        self.strength_max = 1

        self.__stamina = 50
        self.stamina_max = 50
        self.stamina_regen = 1

        self.magic_power = 1 # is multiplied by
        self.spells: list[Spell] = [SPARK, POISON_DART, TELEKINESIS]
        self.__mana = 25
        self.mana_max = 25
        self.mana_regen = 1

        self.evasion = 0.01
        self.evasion_max = 0.01

        self.armor = 0.0
        self.armor_max = 0.0
        self.defend_armor = 1
        self.defend_armor_active = 0 #active at the moment. Adds defend_armor when activated
        self.defend_armor_duration = 1

        self.vulnerability = {
            "normal" : 1.0,
            "fire" : 1.0,
            "ice" : 1.0,
            "electric" : 1.0,
            "bleed" : 1.0,
            "poison" : 1.0,
            "stun" : 1.0
        }

        self.state_effects = self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES} # shows state effects - [dmg, num_rounds_left]
        # for defend its [0, num_rounds left], dmg reduced by defend set in self.defend_armor

        self.items = {
            HEALTH_SYRINGE : 3,
            STAMINA_CARTRIDGE : 4,
            MANA_NANOBOTS : 2
        }


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

    @property
    def attack_power(self):
        return self.strength * self.weapon.damage

    @property
    def attack_stamina_cost(self):
        return self.weapon.cost


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

        adjusted_attack_power = self.attack_power * enemy.vulnerability[self.weapon.type]
        actual_damage = enemy.take_damage(adjusted_attack_power)
        message = random.choice(WEAPON_ATTACK_MESSAGES[self.weapon]).format(enemy=enemy.name, damage=actual_damage)

        if enemy.vulnerability[self.weapon.type] > 1:
            message += " Critical hit!"
        elif enemy.vulnerability[self.weapon.type] < 0.9:
            message += " Not very effective..."
        else:
            message += ""

        return message

    def cast_spell(self, enemy, spell) -> str:
        self.mana -= spell.cost #acceses the mana cost

        #Evasion check
        if self.enemy_evades(enemy):
            message = random.choice(enemy.evade_messages)
            return message

        spell_adjusted = copy.deepcopy(spell)
        spell_adjusted.damage *= self.magic_power
        spell_adjusted.damage *= enemy.vulnerability[spell.type]
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
        if enemy.vulnerability[spell.type] > 1:
            message += " Critical hit!"
        elif enemy.vulnerability[spell.type] < 0.9:
            message += " Not very effective..."
        else:
            message += ""

        return message

    def use_item(self, item, enemy) -> str:
            if self.items.get(item, 0) <= 0:
                return f"You don't have any {item.name}."
            message = item.use(self, enemy)
            self.items[item] -= 1
            if self.items[item] == 0:
                del self.items[item]
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

    def revive(self): #TODO what happens when player dies (restore stats, choose what to keep etc.)
        pass
