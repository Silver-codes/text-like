TEXT_SPEED_SLOW = 0.1
TEXT_SPEED_MEDIUM = 0.065
TEXT_SPEED_FAST = 0.01

EFFECT_TYPES = ("fire", "poison", "stun")
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

EFFECT_EMOJIS = {
    "fire": ":fire:",
    "poison": ":skull_and_crossbones:",
    "stun": ":dizzy:",
}


#Player starting stats
PLAYER_STARTING_HEALTH = 100

PLAYER_STARTING_ATTACK_POWER = 3
PLAYER_STARTING_ATTACK_STAMINA_COST = 5

PLAYER_STARTING_MAGICK_POWER = 1
PLAYER_STARTING_MANA = 25
PLAYER_STARTING_MANA_REGEN = 1

PLAYER_STARTING_STAMINA = 50
PLAYER_STARTING_STAMINA_REGEN = 1

PLAYER_STARTING_EVASION = 0.0

PLAYER_STARTING_ARMOR = 0.0

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


#Enemy starting stats
ENEMY_VULNERABILITY = {
    "normal" : 1,
    "fire" : 1,
    "ice" : 1,
    "electric" : 1,
    "bleed" : 1,
    "poison" : 1,
    "stun" : 1
}

#Unit 7-Null
ENEMY_UNIT7_HEALTH = 12
ENEMY_UNIT7_HEALTH_REGEN = 0
ENEMY_UNIT7_ATTACK_POWER = 2
ENEMY_UNIT7_MAGICK_POWER = 1
ENEMY_UNIT7_EVASION = 0.0
ENEMY_UNIT7_ARMOR = 0
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

ENEMY_UNIT7_ATTACK_MESSAGES = [
    "Unit 7-Null slashes you for {damage} dmg",
    "Unit 7-Null falls onto you for {damage} dmg",
    "Unit 7-Null throws a rock at you for {damage} dmg"
]
