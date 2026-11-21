#spell: (damage, cost, type, effect damage, effect length)


class Spell:
    card_type = "Spell"
    card_color = "blue"
    def __init__(self, name, description, damage, cost, type, effect_damage, effect_length) -> None:
        self.name = name
        self.description = description
        self.damage = damage
        self.cost = cost
        self.type = type
        self.effect_damage = effect_damage
        self.effect_length = effect_length

### Spells - level 1 ###

SPARK = Spell(
    "Spark",
    "Sets your enemy on fire with sparks dealing damage over time",
    1, 5, "fire", 1, 3)
ELECTRIC_PULSE = Spell(
    "Electric Pulse",
   "Shocks enemy with light electric shock",
   2, 4, "electric", 0, 0)
POISON_DART = Spell(
    "Poison Dart",
    "Poison your enemy dealing damage over time",
    0, 3, "poison", 2, 4)



### Spells - level 2 ###
STUN = Spell(
    "Stun",
    "Prevents enemy action",
    0, 5, "stun", 0, 1)
FIREBALL = Spell(
    "Fireball",
    "Hurl a fireball at an enemy, setting him on fire",
    4, 10, "fire", 2, 3)
POISON_SPIKE = Spell(
    "Poison Spike",
    "Applies strong poison to your enemy",
    0, 8, "poison", 2, 4)
FROST_BEAM = Spell(
    "Frost Beam",
    "Make your enemy wish it wore a sweater",
    6, 7, "ice", 0, 0)

### Spells - level 3 ###
SEMPRA_SECTUM = Spell(
    "Sempra Sectum",
    "For enemies",
    12, 10, "bleed", 4, 3)
TELEKINESIS = Spell(
    "Telekinesis",
    "Lift your enemy and perform a delicate bone-breaking smash",
    30, 15, "normal", 0, 0)

### Spell lists ###
ALL_SPELLS = [
    SPARK,
    POISON_DART,
    FIREBALL,
    FROST_BEAM,
    ELECTRIC_PULSE,
    POISON_SPIKE,
    SEMPRA_SECTUM,
    STUN,
    TELEKINESIS
]

SPELLS_IN_LEVELS = {
    "level1": [SPARK, ELECTRIC_PULSE, POISON_DART],
    "level2": [STUN, FIREBALL, POISON_SPIKE, FROST_BEAM],
    "level3": [SEMPRA_SECTUM, TELEKINESIS]

}

### Spell Cast Messages ###
SPELL_CAST_MESSAGES_PLAYER = {
    SPARK : [
        "You project Sparks at {enemy} dealing {damage} dmg. {enemy} starts to burn.",
        "You set {enemy} on fire with Sparks dealing {damage} dmg. {enemy} starts to burn."
    ],
    POISON_DART : [
        "You shoot a Poison Dart at {enemy}. {enemy} is poisoned.",
        "Your Poison Dart hits {enemy}. {enemy} is poisoned."
    ],
    FIREBALL : [
        "You hurled a Fireball at {enemy} for {damage} dmg. {enemy} starts to burn.",
        "You threw a Fireball at {enemy} for {damage} dmg. {enemy} starts to burn."
    ],
    FROST_BEAM : [
        "You projected a Frost Beam at at {enemy} for {damage} dmg."
    ],
    ELECTRIC_PULSE : [
        "You shocked {enemy} with Electric Pulse for {damage} dmg."
    ],
    POISON_SPIKE : [
        "You stabbed {enemy} with Poison Spike for {damage} dmg. {enemy} is poisoned."
    ],
    STUN : [
        "You stunned {enemy}."
    ],
    SEMPRA_SECTUM : [
        "Giant cut wounds appear on {enemy} dealing {damage} dmg. {enemy} starts to bleed."
    ],
    TELEKINESIS : [
        "You use Telekinesis to throw {enemy} against a wall dealing {damage} dmg.",
        "You lift {enemy} and slam him to the ground dealing {damage} dmg."
    ]

}
