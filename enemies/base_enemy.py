import copy
import random
from posix import stat

from constants import (
    EFFECT_MESSAGES_ENEMY,
    EFFECT_TYPES,
    OFFENSIVE_ACTIONS,
    PLAYER_EVASION_MESSAGES,
)
from spells import (
    ELECTRIC_PULSE,
    FIREBALL,
    FROST_BEAM,
    POISON_SPIKE,
    Spell,
)


class Enemy:
    name = "Test Enemy"
    revivals = 10

    health_max = 20
    health_regen = 0

    attack_power = 3
    attack_stamina_cost = 2

    stamina_max = 50
    stamina_regen = 5

    magic_power = 1.0 #is multiplied
    mana_max = 40
    mana_regen = 2

    evasion = 0.0 #is multiplied

    armor = 0

    defend_armor = 1
    defend_stamina_cost = 1
    defend_armor_duration = 1




    def __init__(self) -> None:
        self.health = self.health_max
        self.stamina = self.stamina_max
        self.mana = self.mana_max
        self.defend_armor_active = 0
        self.is_stunned = False

        self.spells: list[Spell] = [FIREBALL, FROST_BEAM, ELECTRIC_PULSE, POISON_SPIKE]
        self.vulnerability = {
            "normal" : 1,
            "fire" : 3,
            "ice" : 1,
            "electric" : 1,
            "bleed" : 1,
            "poison" : 1,
            "stun" : 1
        }
        self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES} # shows state effects - [dmg, num_rounds_left]
        self.attack_messages = [f"{self.name} attacks you for {self.attack_power} dmg"]
        self.defend_messages = [f"{self.name} defends"]
        self.rest_messages = [f"{self.name} rests"]
        self.evade_messages = [f"{self.name} evades"]
        self.actions = ["attack", "cast_spell", "defend", "rest"]
        self.action_weights = {
            "attack" : 1,
            "cast_spell" : 1,
            "defend" : 1,
            "rest" : 1
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

    ### Methods ###
    def take_damage(self, damage_taken: float):
        actual_damage = (damage_taken) - (self.armor + self.defend_armor_active) #calculates damage minus armor and defending
        actual_damage = round(actual_damage) # rounding, cause I want only integer hp
        actual_damage = max(actual_damage, 0) #actual dmg can't be negative
        self.health -= actual_damage
        return actual_damage


    def attack(self, player):
        actual_damage = player.take_damage(self.attack_power)
        self.stamina -= self.attack_stamina_cost
        message = random.choice(self.attack_messages).format(damage=actual_damage)
        return message


    def cast_spell(self, player, spell):
        spell_adjusted = copy.deepcopy(spell)
        spell_adjusted.damage *= self.magic_power
        spell_adjusted.damage *= player.vulnerability[spell.type]
        spell_adjusted.damage = round(spell_adjusted.damage)
        spell_adjusted.effect_damage *= self.magic_power
        spell_adjusted.effect_damage *= player.vulnerability[spell.type]
        spell_adjusted.effect_damage = round(spell_adjusted.effect_damage)
        actual_damage = player.take_damage(spell_adjusted.damage)

        #State effects
        if spell.type in EFFECT_TYPES:
            effect_damage_adjusted = round(spell.effect_damage * player.vulnerability[spell.type])
            player.state_effects[spell.type] = [effect_damage_adjusted, spell.effect_length]

        self.mana -= spell.cost
        message = f"{self.name} casts {spell.name} dealing {actual_damage} dmg"
        return message

    def defend(self):
        self.stamina -= self.defend_stamina_cost
        # defending also regenerates a half as much as rest
        mana_regenerated = round(self.mana_regen / 2)
        self.mana += mana_regenerated
        stamina_regenerated = round(self.stamina_regen / 2)
        self.stamina += stamina_regenerated
        self.defend_armor_active = self.defend_armor
        self.state_effects["defend"] = [0, self.defend_armor_duration + 1] # plus one cause enemy defends right before refresh calls
        return random.choice(self.defend_messages).format(stamina=stamina_regenerated, mana=mana_regenerated)

    def rest(self):
        self.mana += self.mana_regen
        self.stamina += self.stamina_regen
        return random.choice(self.rest_messages).format(stamina=self.stamina_regen, mana=self.mana_regen)


    # Enemy AI logic
    def take_turn(self, player):
        assert set(self.actions) == set(self.action_weights), f"{self.name}: actions and weights don't match" # checks for those two lists, if they have same keys
        affordable_spells = [spell for spell in self.spells if spell.cost <= self.mana]
        available_actions = []
        if "attack" in self.actions and self.attack_stamina_cost <= self.stamina:
            available_actions.append("attack")
        if "cast_spell" in self.actions and affordable_spells:
            available_actions.append("cast_spell")
        if "defend" in self.actions and self.defend_stamina_cost <=self.stamina and self.state_effects["defend"][1] == 0:
            available_actions.append("defend")
        if not available_actions:
            available_actions.append("rest")

        weights = [self.action_weights[action] for action in available_actions]
        action = random.choices(available_actions, weights)[0] #the first chosed

        # Player evasion check
        if action in OFFENSIVE_ACTIONS and self.player_evades(player):
            return random.choice(PLAYER_EVASION_MESSAGES).format(name=self.name)

        if action == "attack":
            message = self.attack(player)
        elif action == "cast_spell":
            spell = random.choice(self.spells)
            message = self.cast_spell(player, spell)
        elif action == "defend":
            message = self.defend()
        elif action == "rest":
            message = self.rest()
        else:
            raise ValueError(f"ENEMY CHOSE {action} UNEXPECTEDLY.")
        return message

    def player_evades(self, player) -> bool:
        return random.random() < player.evasion

    def refresh(self): #actions that happen at the end of every round
        message = ""
        # Regeneration
        if self.health < self.health_max:
            self.health += self.health_regen
            if self.health_regen != 0:
                message += f"{self.name} regenerated {self.health_regen}hp. "

        # State effects (burn, poison)
        for effect, (damage, duration) in self.state_effects.items():
                if duration <= 0:
                    continue
                self.health -= damage
                if effect in EFFECT_MESSAGES_ENEMY:
                    message += f"{EFFECT_MESSAGES_ENEMY[effect].format(name=self.name,damage=damage)} "
                self.state_effects[effect][1] -= 1
        if self.state_effects["defend"] == [0, 0]:
            self.defend_armor_active = 0
        return message
