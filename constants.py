from spells import FIREBALL

TEXT_SPEED_SLOW = 0.1
TEXT_SPEED_MEDIUM = 0.065
TEXT_SPEED_FAST = 0.01

PLAYER_ATTACK_MESSAGES = [
    "You hit {enemy} for {damage} damage.",
    "You punched {enemy} for {damage} damage.",
    "You dealt {damage} damage to your enemy"
]

EFFECT_MESSAGES_ENEMY = {
    "fire": "{name} burns for {damage} dmg.",
    "poison": "{name} is poisoned for {damage} dmg.",
    "stun": "{name} is stunned.",
}
EFFECT_MESSAGES_PLAYER = {
    "fire": "You burn for {damage} dmg. ",
    "poison": "You are poisoned for {damage} dmg.",
    "stun": "You sare stunned.",
}

EFFECT_TYPES = ("fire", "poison", "stun", "defend")
EFFECT_EMOJIS = {
    "fire": ":fire:",
    "poison": ":skull_and_crossbones:",
    "stun": ":dizzy:",
    "defend": ":shield:",
}
OFFENSIVE_ACTIONS = {"attack", "cast_spell"}

LOST_BATTLE_MESSAGES = [
    "You have perished.",
    "{name} crushed you.",
    "YOU DIED",
    "You have been obliterated by {name}.",
    "You didn't stand a chance.",
    "{name} was just better.",
    "You didn't stand a chance against {name}.",
    "AGAIN?!",
    "You have been defeated.",
    "You lost.",
    "You failed.",
    "You disappointed."
]

WON_BATTLE_MESSAGES = [
    "You won.",
    "You are victorious.",
    "You defeated {name}.",
    "You outlasted {name}.",
    "{name} has been defeated.",
    "You emerged victorious.",
    "Victory is yours.",
    "You won. But at what cost?",
    "You bested {name}."
]

#Player starting stats
PLAYER_STARTING_HEALTH = 100

PLAYER_STARTING_ATTACK_POWER = 3
PLAYER_STARTING_ATTACK_STAMINA_COST = 5

PLAYER_STARTING_MAGICK_POWER = 1
PLAYER_STARTING_MANA = 25
PLAYER_STARTING_MANA_REGEN = 1

PLAYER_STARTING_STAMINA = 50
PLAYER_STARTING_STAMINA_REGEN = 1

PLAYER_STARTING_EVASION = 0.05

PLAYER_STARTING_ARMOR = 0.0
PLAYER_STARTING_DEFEND_ARMOR = 1
PLAYER_STARTING_DEFEND_ARMOR_DURATION = 1

PLAYER_STARTING_VULNERABILITY = {
    "normal" : 1.0,
    "fire" : 1.0,
    "ice" : 1.0,
    "electric" : 1.0,
    "bleed" : 1.0,
    "poison" : 1.0,
    "stun" : 1
}

PLAYER_LOW_HEALTH_THRESHOLD = 20 #at what % of health is damage taken lower
PLAYER_LOW_HEALTH_ADVANTAGE = 0.66 #damage taken when under threshold - MUST BE ABOVE 0.5

PLAYER_EVASION_MESSAGES = [
    "You evaded the attack",
    "{name} misses.",
]


#Enemy starting stats
ENEMY_VULNERABILITY = {
    "normal" : 1,
    "fire" : 3,
    "ice" : 1,
    "electric" : 1,
    "bleed" : 1,
    "poison" : 1,
    "stun" : 1
}

####################   1 Unit 7-Null   ####################
ENEMY_UNIT7_HEALTH = 12
ENEMY_UNIT7_HEALTH_MAX = 12
ENEMY_UNIT7_HEALTH_REGEN = 0

ENEMY_UNIT7_ATTACK_POWER = 2
ENEMY_UNIT7_ATTACK_STAMINA_COST = 3

ENEMY_UNIT7_STAMINA = 10
ENEMY_UNIT7_STAMINA_MAX = 10
ENEMY_UNIT7_STAMINA_REGEN = 2

ENEMY_UNIT7_MAGICK_POWER = 1
ENEMY_UNIT7_MANA = 10
ENEMY_UNIT7_MANA_MAX = 10
ENEMY_UNIT7_MANA_REGEN = 2
ENEMY_UNIT7_SPELLS = [FIREBALL]

ENEMY_UNIT7_EVASION = 0.01
ENEMY_UNIT7_ARMOR = 0

ENEMY_UNIT7_DEFEND_ARMOR = 1
ENEMY_UNIT7_DEFEND_ARMOR_DURATION = 1
ENEMY_UNIT7_DEFEND_STAMINA_COST = 3

ENEMY_UNIT7_VULNERABILITY = {
    "normal" : 1.0,
    "fire" : 1.0,
    "ice" : 1.0,
    "electric" : 1.6,
    "bleed" : 0.3,
    "poison" : 0.3,
    "stun" : 1
}
ENEMY_UNIT7_STATE_EFFECTS = {effect: [0, 0] for effect in EFFECT_TYPES}

ENEMY_UNIT7_ACTIONS = ["attack", "cast_spell", "defend", "rest"]
ENEMY_UNIT7_ACTION_WEIGHTS = { #IMPORTANT - defines enemy behaviour, can't use 0
    "attack" : 10,
    "cast_spell" : 4,
    "defend" : 2,
    "rest" : 1
}

ENEMY_UNIT7_ATTACK_MESSAGES = [
    "Unit 7-Null slashes you for {damage} dmg",
    "Unit 7-Null falls onto you for {damage} dmg",
    "Unit 7-Null throws a rock at you for {damage} dmg"
]

ENEMY_UNIT7_DEFEND_MESSAGES = [
    "Unit 7-Null braces for impact. +{stamina} stamina, +{mana} energy",
    "Unit 7-Null curles in a ball. +{stamina} stamina, +{mana} energy",
    "Unit 7-Null covers. +{stamina} stamina, +{mana} energy"
]

ENEMY_UNIT7_REST_MESSAGES = [
    "Unit 7-Null is out of power. +{stamina} stamina, +{mana} energy",
    "Unit 7-Null is regaining power. +{stamina} stamina, +{mana} energy",
    "Unit 7-Null needs maintenance. +{stamina} stamina, +{mana} energy"
]

ENEMY_UNIT7_EVADE_MESSAGES = [
    "Unit 7-Null trips and avoides your attack.",
    "Unit 7-Null twitches and accidentaly avoids your attack.",
    "Unit 7-Null's spastick movement causes you to miss."
]
