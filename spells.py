#Dict of all spells in order: spell: (damage, cost)


class Spell:
    def __init__(self, name, damage, cost, effect) -> None:
        self.name = name
        self.damage = damage
        self.cost = cost
        self.effect = effect

FIREBALL = Spell("Fireball", 10, 5, "fire")
FROST_BEAM = Spell("Frost Beam", 6, 3, "ice")
ELECTRIC_PULSE = Spell("Electric Pulse", 2, 2, "electric")
