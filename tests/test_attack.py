import sys
sys.path.insert(0, "../")  # add Folder_2 path to search list

from enemies import Enemy
from player import Player

player = Player()
enemy = Enemy()
print(f"Player health {player.health}")
print(f"Enemy health {enemy.health}")
print()


player.attack(enemy)
print("player attacks enemy")
print(f"Player health {player.health}")
print(f"Player stamina {player.stamina}")
print(f"Enemy health {enemy.health}")
print(f"Enemy stamina {enemy.stamina}")

print()
enemy.attack(player)
print("enemy attacks player")
print(f"Player health {player.health}")
print(f"Player stamina {player.stamina}")
print(f"Enemy health {enemy.health}")
print(f"Enemy stamina {enemy.stamina}")
