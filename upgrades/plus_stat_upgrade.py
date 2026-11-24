from upgrades.base_upgrade import Upgrade


class PlusStatUpgrade(Upgrade):
    STATS = ("health", "stamina", "mana", "armor", "evasion")

    def __init__(self, name, description, stat, stat_max, amount):
        super().__init__(name, description)
        if stat not in self.STATS:
            raise ValueError(f"{name}: unknown stat '{stat}'")
        self.stat = stat
        self.stat_max = stat_max
        self.amount = amount

    def apply(self, player):
        current = getattr(player, self.stat)
        current_max = getattr(player, self.stat_max)
        amount_to_add = (self.amount / current_max) * current
        new_max = round(current_max + self.amount)
        new_value = round(current + amount_to_add)
        setattr(player, self.stat_max, new_max)
        setattr(player, self.stat, new_value)


### Level 1 ###
HEALTH_BOOST1 = PlusStatUpgrade(
    "Health Boost *",
    "+5 max health",
    "health",
    "health_max",
    5)

STAMINA_BOOST1 = PlusStatUpgrade(
    "Stamina Boost *",
    "+3 max stamina",
    "stamina",
    "stamina_max",
    3)

MANA_BOOST1 = PlusStatUpgrade(
    "Mana Boost *",
    "+3 max mana",
    "mana",
    "mana_max",
    3)

ARMOR_BOOST1 = PlusStatUpgrade(
    "Armor Boost *",
    "+1 armor",
    "armor",
    "armor_max",
    1)

EVASION_BOOST1 = PlusStatUpgrade(
    "Evasion Boost *",
    "+1% chance of evasion",
    "evasion",
    "evasion_max",
    0.01)


### Level 2 ###
HEALTH_BOOST2 = PlusStatUpgrade(
    "Health Boost **",
    "+15 max health",
    "health",
    "health_max",
    15)

STAMINA_BOOST2 = PlusStatUpgrade(
    "Stamina Boost **",
    "+8 max stamina",
    "stamina",
    "stamina_max",
    8)

MANA_BOOST2 = PlusStatUpgrade(
    "Mana Boost **",
    "+7 max mana",
    "mana",
    "mana_max",
    7)

ARMOR_BOOST2 = PlusStatUpgrade(
    "Armor Boost **",
    "+2 armor",
    "armor",
    "armor_max",
    2)

EVASION_BOOST2 = PlusStatUpgrade(
    "Evasion Boost **",
    "+2% chance of evasion",
    "evasion",
    "evasion_max",
    0.02)

### Level 3 ###
HEALTH_BOOST3 = PlusStatUpgrade(
    "Health Boost ***",
    "+30 max health",
    "health",
    "health_max",
    30)

STAMINA_BOOST3 = PlusStatUpgrade(
    "Stamina Boost ***",
    "+15 max stamina",
    "stamina",
    "stamina_max",
    15)

MANA_BOOST3 = PlusStatUpgrade(
    "Mana Boost ***",
    "+13 max mana",
    "mana",
    "mana_max",
    13)

ARMOR_BOOST3 = PlusStatUpgrade(
    "Armor Boost ***",
    "+4 armor",
    "armor",
    "armor_max",
    2)

EVASION_BOOST3 = PlusStatUpgrade(
    "Evasion Boost ***",
    "+3% chance of evasion",
    "evasion",
    "evasion_max",
    0.03)
