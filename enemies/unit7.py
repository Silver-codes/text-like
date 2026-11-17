####################   1 Unit 7-Null   ####################

from constants import EFFECT_TYPES
from enemies.base_enemy import Enemy
from spells import SPARK, Spell


class EnemyUnit7(Enemy):
    name = "Unit 7-Null"
    revivals = None
    num_defeated = 0

    health_max = 20
    health_regen = 0

    attack_power = 3
    attack_stamina_cost = 4

    stamina_max = 10
    stamina_regen = 2

    mana_max = 10
    mana_regen = 2
    magic_power = 1 #is multiplied

    evasion = 0.005

    armor = 0
    defend_armor = 1
    defend_armor_duration = 1
    defend_stamina_cost = 3


    def __init__(self):
        super().__init__()
        self.defend_armor_active = 0
        self.is_stunned = False

        self.spells: list[Spell] = [SPARK]

        self.vulnerability = {
            "normal" : 1.0,
            "fire" : 1.0,
            "ice" : 1.0,
            "electric" : 1.6,
            "bleed" : 0.3,
            "poison" : 0.3,
            "stun" : 1
        }

        self.state_effects = {effect: [0, 0] for effect in EFFECT_TYPES}

        self.actions = ["attack", "cast_spell", "defend", "rest"]
        self.action_weights = { #IMPORTANT - defines enemy behaviour, can't use 0
            "attack" : 10,
            "cast_spell" : 4,
            "defend" : 2,
            "rest" : 1
        }

        self.attack_messages = [
            "Unit 7-Null slashes you for {damage} dmg.",
            "Unit 7-Null falls onto you for {damage} dmg.",
            "Unit 7-Null throws a rock at you for {damage} dmg."
        ]

        self.defend_messages = [
            "Unit 7-Null braces for impact. +{stamina} stamina, +{mana} energy.",
            "Unit 7-Null curls in a ball. +{stamina} stamina, +{mana} energy.",
            "Unit 7-Null covers. +{stamina} stamina, +{mana} energy."
        ]

        self.rest_messages = [
            "Unit 7-Null is out of power. +{stamina} stamina, +{mana} energy.",
            "Unit 7-Null is regaining power. +{stamina} stamina, +{mana} energy.",
            "Unit 7-Null needs maintenance. +{stamina} stamina, +{mana} energy."
        ]

        self.evade_messages = [
            "Unit 7-Null trips and avoids your attack.",
            "Unit 7-Null twitches and accidentally avoids your attack.",
            "Unit 7-Null's spastic movement causes you to miss."
        ]

        self.intro_sequence_texts = [
            """
You hear robotic movement somewhere in the darkness ahead of you. Slow clunky irregular steps,
wiring sounds, small electro-motors steadily closing in on your location.\n
Then you see it.\n
[red]A faint red light pulsing.[/red]\n
It's metallic humanoid body slowly emerges from the back of the room, lighting its way
by a small red LED in a place where eyes would normally reside.\n
Across its chestplate you read red indentet text. [bold red]Unit 7-Null[/bold red].
There's one more thing to read. Bolted to its upper left chest is a small plastic ID tag reads: Tobias Wyrick.\n
[italic]The name is human, but the thing is definitely not.\n
As it closes the distance, you can tell it wants to fight. It wants to kill.\n
[italic]Can the thing even want something?[/italic]\n
[bold red]This isn't a fucking phylosophy lesson. You need to fight for your life.[/bold red]\n""",
f"{self.name} approaches you from the darkness, looking for a fight",
f"It's that humanoid monster {self.name} again.",
f"You've seen this before, it's {self.name}. This should be over soon",
f"{self.name} appears in front of you, ready for another beating.",
f"{self.name} appears again. Who keeps putting it back together?",
"Unit 7-Null stumbles forth. [bold red]I'm getting fucking tired of fighting you![/bold red]",
"Unit 7-Null emerges. [bold red]I'll make goddamn sure you won't get back up again![/bold red]",
"Seeing Unit 7-Null again your blood starts to boil. [bold red]You're not getting back up this time![/bold red]",
        ]
