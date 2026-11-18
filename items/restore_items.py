from items.base_item import Item


class RestoreItem(Item):
    STATS = ("health", "stamina", "mana")

    def __init__(self, name, description, used_message, stat, amount):
        super().__init__(name, description, used_message)
        if stat not in self.STATS:
            raise ValueError(f"{name}: unknown stat '{stat}'")
        self.stat = stat
        self.amount = amount

    def use(self, player, enemy):
        current = getattr(player, self.stat)
        setattr(player, self.stat, current + self.amount)
        message = self.used_message.format(name=self.name, amount=self.amount, stat=self.stat)
        return message

### Level 1 ###
HEALTH_SYRINGE = RestoreItem(
    "Health Syringe",
    "Restores +10 health",
    "You injected {name} into your arm. +{amount} {stat}.",
    "health",
    10)

STAMINA_SYRINGE = RestoreItem(
    "Stamina Syringe",
    "Restores +8 stamina",
    "You injected {name} into your arm. +{amount} {stat}.",
    "stamina",
    8)

MANA_SYRINGE = RestoreItem(
    "Mana Syringe",
    "Restores +6 mana",
    "You injected {name} into your arm. +{amount} {stat}.",
    "mana",
    6)


### Level 2 ###
HEALTH_CARTRIDGE = RestoreItem(
    "Health Cartridge",
    "Restores +25 health",
    "You draw out of {name}. +{amount} {stat}.",
    "health",
    25)

STAMINA_CARTRIDGE = RestoreItem(
    "Stamina Cartridge",
    "Restores +15 stamina",
    "You draw out of {name}. +{amount} {stat}.",
    "stamina",
    15)

MANA_CARTRIDGE = RestoreItem(
    "Mana Cartridge",
    "Restores +12 mana",
    "You draw out of {name}. +{amount} {stat}.",
    "mana",
    12)


### Level 3 ###
HEALTH_NANOBOTS = RestoreItem(
    "Health Nanobots",
    "Restores full health",
    "You let {name} crawl under your skin. Restores full {stat}",
    "health",
    10000)

STAMINA__NANOBOTS = RestoreItem(
    "Stamina Nanobots",
    "Restores full stamina",
    "You let {name} crawl under your skin. Restores full {stat}",
    "stamina",
    10000)

MANA_NANOBOTS = RestoreItem(
    "Mana Nanobots",
    "Restores full mana",
    "You let {name} crawl under your skin. Restores full {stat}",
    "mana",
    10000)
