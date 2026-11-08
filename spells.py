#Dict of all spells in order: spell: (damage, cost)

spells = {
    "Fireball":(10, 5),
    "Frost Beam":(6,3)
}

class Spell:
    def __init__(self, name, damage, cost) -> None:
        self.name = name
        self.damage = damage
        self.cost = cost

FIREBALL = Spell("Fireball", 10, 5)
FROST_BEAM = Spell("Frost Beam", 6, 3)
