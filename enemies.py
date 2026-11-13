import copy
import random
from posix import stat

from constants import (
    EFFECT_MESSAGES_ENEMY,
    EFFECT_TYPES,
    ENEMY_UNIT7_ACTIONS,
    ENEMY_UNIT7_ARMOR,
    ENEMY_UNIT7_ATTACK_MESSAGES,
    ENEMY_UNIT7_ATTACK_POWER,
    ENEMY_UNIT7_DEFEND_ARMOR,
    ENEMY_UNIT7_DEFEND_ARMOR_DURATION,
    ENEMY_UNIT7_DEFEND_MESSAGES,
    ENEMY_UNIT7_EVASION,
    ENEMY_UNIT7_HEALTH,
    ENEMY_UNIT7_HEALTH_MAX,
    ENEMY_UNIT7_HEALTH_REGEN,
    ENEMY_UNIT7_MAGICK_POWER,
    ENEMY_UNIT7_MANA,
    ENEMY_UNIT7_MANA_MAX,
    ENEMY_UNIT7_MANA_REGEN,
    ENEMY_UNIT7_REST_MESSAGES,
    ENEMY_UNIT7_STAMINA,
    ENEMY_UNIT7_STAMINA_MAX,
    ENEMY_UNIT7_STAMINA_REGEN,
    ENEMY_UNIT7_STATE_EFFECTS,
    ENEMY_UNIT7_VULNERABILITY,
    ENEMY_VULNERABILITY,
)
from spells import (
    ELECTRIC_PULSE,
    FIREBALL,
    FROST_BEAM,
    NO_SPELL,
    POISON_SPIKE,
    STUN,
    Spell,
)


class Enemy:
    def __init__(self) -> None:
        self.name = "Test Enemy"

        self.health_max = 20
        self.__health = 20
        self.health_regen = 0

        self.attack_power = 3
        self.attack_stamina_cost = 8

        self.__stamina = 50
        self.stamina_max = 50
        self.stamina_regen = 5

        self.magic_power = 1
        self.__mana = 40
        self.mana_max = 40
        self.mana_regen = 2
        self.spells: list[Spell] = [FIREBALL, FROST_BEAM, ELECTRIC_PULSE, POISON_SPIKE]

        self.evasion = 0.0
        self.armor = 0

        self.vulnerability = ENEMY_VULNERABILITY
        self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES} # shows state effects - [dmg, num_rounds_left]
        self.attack_messages = [f"{self.name} attacks you for {self.attack_power} dmg"]
        self.defend_messages = [f"{self.name} defends"]
        self.rest_messages = [f"{self.name} rests"]
        self.defend_armor = 1
        self.defend_armor_active = 0
        self.defend_armor_duration = 1
        self.actions = ["attack", "cast_spell", "defend"]

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

    ### Methods ###
    def take_damage(self, damage_taken: float, spell):
        if self.evasion < random.random(): #checks if evades
            actual_damage = (damage_taken * self.vulnerability[spell.type]) - (self.armor + self.defend_armor_active) #calculates damage times vuln, minus armor
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
        return 0, "Enemy evaded the attack", {} # TODO enemy evasion comunicated to player

    def attack(self, player):
        actual_damage = player.take_damage(self.attack_power, NO_SPELL)
        self.stamina -= self.attack_stamina_cost
        message = random.choice(self.attack_messages).format(damage=actual_damage)
        return message


    def cast_spell(self, player, spell):
        spell_adjusted = copy.deepcopy(spell)
        spell_adjusted.damage *= self.magic_power
        spell_adjusted.damage = round(spell_adjusted.damage)
        spell_adjusted.effect_damage *= self.magic_power
        spell_adjusted.effect_damage = round(spell_adjusted.effect_damage)
        actual_damage = player.take_damage(spell_adjusted.damage, spell_adjusted)
        self.mana -= spell.cost
        message = f"{self.name} casts {spell.name} dealing {actual_damage} dmg"
        return message

    def defend(self):
        self.defend_armor_active = self.defend_armor
        self.state_effects["defend"] = [0, self.defend_armor_duration + 1] # plus one cause enemy defends right before refresh calls
        return random.choice(self.defend_messages)

    def rest(self):
        self.mana += self.mana_regen
        self.stamina += self.stamina_regen
        return random.choice(self.rest_messages).format(stamina=self.stamina_regen, mana=self.mana_regen)


    # Enemy AI logic
    def take_turn(self, player):
        action = random.choice(self.actions)
        if action == "attack":
            message = self.attack(player)
        elif action == "cast_spell":
            spell = random.choice(self.spells)
            message = self.cast_spell(player, spell)
        elif action == "defend":
            message = self.defend()
        elif action == "rest":
            message = self.rest()
        return message

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
                if effect in EFFECT_MESSAGES_ENEMY:
                    message += EFFECT_MESSAGES_ENEMY[effect].format(damage=damage)
                self.state_effects[effect][1] -= 1
        if self.state_effects["defend"] == [0, 0]:
            self.defend_armor_active = 0
        return message

####################   1 Unit 7-Null   ####################
class Enemy_Unit7(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Unit 7-Null"
        self.revivals = "N/A"

        self.health_max = ENEMY_UNIT7_HEALTH_MAX
        self.health = ENEMY_UNIT7_HEALTH
        self.health_regen = ENEMY_UNIT7_HEALTH_REGEN

        self.attack_power = ENEMY_UNIT7_ATTACK_POWER

        self.stamina_max = ENEMY_UNIT7_STAMINA_MAX
        self.stamina = ENEMY_UNIT7_STAMINA
        self.stamina_regen = ENEMY_UNIT7_STAMINA_REGEN

        self.magic_power = ENEMY_UNIT7_MAGICK_POWER
        self.spells: list[Spell] = [FIREBALL, FROST_BEAM, ELECTRIC_PULSE, POISON_SPIKE]
        self.mana_max = ENEMY_UNIT7_MANA_MAX
        self.mana = ENEMY_UNIT7_MANA
        self.mana_regen = ENEMY_UNIT7_MANA_REGEN

        self.evasion = ENEMY_UNIT7_EVASION

        self.armor = ENEMY_UNIT7_ARMOR
        self.defend_armor = ENEMY_UNIT7_DEFEND_ARMOR
        self.defend_armor_active = 0
        self.defend_armor_duration = ENEMY_UNIT7_DEFEND_ARMOR_DURATION

        self.vulnerability = ENEMY_UNIT7_VULNERABILITY

        self.state_effects = ENEMY_UNIT7_STATE_EFFECTS

        self.is_stunned = False

        self.attack_messages = ENEMY_UNIT7_ATTACK_MESSAGES
        self.defend_messages = ENEMY_UNIT7_DEFEND_MESSAGES
        self.rest_messages = ENEMY_UNIT7_REST_MESSAGES

        self.actions = ENEMY_UNIT7_ACTIONS
