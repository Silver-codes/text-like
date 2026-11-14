####################   1 Unit 7-Null   ####################
from constants import EFFECT_TYPES
from enemies.base_enemy import Enemy
from spells import FIREBALL, Spell


class EnemyUnit7(Enemy):
    name = "Unit 7-Null"
    revivals = None

    health_max = 12
    health_regen = 0

    attack_power = 3
    attack_stamina_cost = 4

    stamina_max = 10
    stamina_regen = 2

    mana_max = 10
    mana_regen = 2
    magic_power = 1 #is multiplied

    evasion = 0.05

    armor = 0
    defend_armor = 1
    defend_armor_duration = 1
    defend_stamina_cost = 3


    def __init__(self):
        super().__init__()
        self.defend_armor_active = 0
        self.is_stunned = False

        self.spells: list[Spell] = [FIREBALL]

        self.vulnerability = {
            "normal" : 1.0,
            "fire" : 1.0,
            "ice" : 1.0,
            "electric" : 1.6,
            "bleed" : 0.3,
            "poison" : 0.3,
            "stun" : 1
        }

        self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES}

        self.actions = ["attack", "cast_spell", "defend", "rest"]
        self.action_weights = { #IMPORTANT - defines enemy behaviour, can't use 0
            "attack" : 10,
            "cast_spell" : 4,
            "defend" : 2,
            "rest" : 1
        }

        self.attack_messages = [
            "Unit 7-Null slashes you for {damage} dmg",
            "Unit 7-Null falls onto you for {damage} dmg",
            "Unit 7-Null throws a rock at you for {damage} dmg"
        ]

        self.defend_messages = [
            "Unit 7-Null braces for impact. +{stamina} stamina, +{mana} energy",
            "Unit 7-Null curls in a ball. +{stamina} stamina, +{mana} energy",
            "Unit 7-Null covers. +{stamina} stamina, +{mana} energy"
        ]

        self.rest_messages = [
            "Unit 7-Null is out of power. +{stamina} stamina, +{mana} energy",
            "Unit 7-Null is regaining power. +{stamina} stamina, +{mana} energy",
            "Unit 7-Null needs maintenance. +{stamina} stamina, +{mana} energy"
        ]

        self.evade_messages = [
            "Unit 7-Null trips and avoids your attack.",
            "Unit 7-Null twitches and accidentally avoids your attack.",
            "Unit 7-Null's spastic movement causes you to miss."
        ]
