class Item:
    card_type = "Item"
    card_color = "green"
    def __init__(self, name: str, description: str, used_message: str):
        self.name = name
        self.description = description
        self.used_message = used_message

    def use(self, player, enemy):
        message = "Used non-existent Base Item"
        return message
