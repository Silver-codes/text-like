class Upgrade:
    card_type = "Upgrade"
    card_color = "purple"
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def apply(self, player):
        pass
