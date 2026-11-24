class Item:
    card_type = "Item"
    card_color = "green"
    def __init__(self, name: str, description: str, used_message: str):
        self.name = name
        self.description = description
        self.used_message = used_message

    def pick_up(self, player):
        if self in player.items:
            player.items[self] += 1
        else:
            player.items[self] = 1
        return f"You gained +1 {self.name}\nYour items are now:\n{", ".join(f"{item.name} x{count}" for item, count in player.items.items())}"

    def use(self, player, enemy):
        message = "Used non-existent Base Item"
        return message
