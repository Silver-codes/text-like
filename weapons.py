#Weapon: (damage, cost, type, effect damage, effect length)


class Weapon:
    def __init__(self, name, damage, cost, type, effect_damage, effect_length) -> None:
        self.name = name
        self.damage = damage
        self.cost = cost
        self.type = type
        self.effect_damage = effect_damage
        self.effect_length = effect_length

FISTS = Weapon("Fists", 3, 3, "normal", 0, 0)



### Spell Cast Messages ###
WEAPON_ATTACK_MESSAGES = {
    FISTS : [
        "You punched {enemy} for {damage} dmg",
        "You tackled {enemy} for {damage} dmg",
        "You clawed at {enemy} for {damage} dmg",
        "You kicked {enemy} for {damage} dmg"
    ]
}
