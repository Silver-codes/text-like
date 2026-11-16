#Weapon: (damage, cost, type, effect damage, effect length)


class Weapon:
    def __init__(self, name, damage, cost, type, effect_damage, effect_length) -> None:
        self.name = name
        self.damage = damage
        self.cost = cost
        self.type = type
        self.effect_damage = effect_damage
        self.effect_length = effect_length

### Weapons - Level 1 ###
FISTS = Weapon("Fists", 2, 3, "normal", 0, 0)
SHIV = Weapon("Shiv", 4, 2, "normal", 0, 0)
BRASS_KNUCKLES = Weapon("Brass Knuckles", 3, 3, "normal", 0, 0)
RUSTY_PIPE = Weapon("Rusty Pipe", 5, 5, "normal", 0, 0)

### Weapons - Level 2 ###


### Weapons - Level 3 ###


### Weapon lists ###
ALL_WEAPONS = [SHIV, BRASS_KNUCKLES, RUSTY_PIPE]
WEAPONS_IN_LEVELS = {
    "level1": [SHIV, BRASS_KNUCKLES, RUSTY_PIPE],
    "level2": [SHIV, BRASS_KNUCKLES, RUSTY_PIPE],
    "level3": [SHIV, BRASS_KNUCKLES, RUSTY_PIPE]

}


### Spell Cast Messages ###
WEAPON_ATTACK_MESSAGES = {
    FISTS : [
        "You punched {enemy} for {damage} dmg.",
        "You tackled {enemy} for {damage} dmg.",
        "You clawed at {enemy} for {damage} dmg.",
        "You kicked {enemy} for {damage} dmg."
    ],
    SHIV : [
        "You slashed {enemy} with your Shiv for {damage} dmg.",
        "You swing your Shiv and cut {enemy} for {damage} dmg.",
        "You Shived {enemy} for {damage} dmg.",
        "You stabbed {enemy} for {damage} dmg."
    ],
    BRASS_KNUCKLES :[
        "You punched {enemy} with Brass Knuckles for {damage} dmg.",
        "Your Brass knuckles dealt {damage} dmg.",
        "{enemy} got fistfull of your Brass Knuckles for {damage} dmg."
    ],
    RUSTY_PIPE : [
        "You swing your Rusty Pipe and hit {enemy} for {damage} dmg.",
        "Your Rusty Pipe vibrates as you hit {enemy} for {damage} dmg.",
        "You hit {enemy} with Rusty Pipe for {damage} dmg."
    ]
}
