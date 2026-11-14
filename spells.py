#Dict of all spells in order: spell: (damage, cost, type, effect damage, effect length)


class Spell:
    def __init__(self, name, damage, cost, type, effect_damage, effect_length) -> None:
        self.name = name
        self.damage = damage
        self.cost = cost
        self.type = type
        self.effect_damage = effect_damage
        self.effect_length = effect_length

NO_SPELL = Spell("NoSpell", 0, 0, "normal", 0, 0)
FIREBALL = Spell("Fireball", 1, 5, "fire", 2, 3)
FROST_BEAM = Spell("Frost Beam", 6, 3, "ice", 0, 0)
ELECTRIC_PULSE = Spell("Electric Pulse", 2, 2, "electric", 0, 0)
POISON_SPIKE = Spell("Poison spike", 0, 2, "poison", 2, 4)
STUN = Spell("Stun", 0, 5, "stun", 0, 3)



### Spell Cast Messages ###
SPELL_CAST_MESSAGES_PLAYER = {
    FIREBALL : [
        "You hurled a Fireball at {enemy} for {damage} dmg",
        "You threw a Fireball at {enemy} for {damage} dmg"
    ],
    FROST_BEAM : [
        "You projected a Frost Beam at at {enemy} for {damage} dmg"
    ],
    ELECTRIC_PULSE : [
        "You shocked {enemy} with Electric Pulse for {damage} dmg"
    ],
    POISON_SPIKE : [
        "You stabbed {enemy} with Poison Spike for {damage} dmg"
    ],
    STUN : [
        "You stunned {enemy}"
    ]
}
