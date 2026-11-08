import random
import time

from rich import print
from rich.live import Live
from rich.text import Text


def shake_text(message: str, duration: float = 0.8):
    """Shakes text violently on screen for a short duration."""
    styles = ["bold red", "bold bright_red", "bold yellow", "white"]
    start_time = time.time()

    with Live(refresh_per_second=25, transient=True) as live:
        while time.time() - start_time < duration:
            # Random horizontal offset (spaces) and random danger style
            spaces = " " * random.randint(0, 3)
            style = random.choice(styles)

            # Render the jittery text
            live.update(Text(f"{spaces}⚡ {message} ⚡", style=style))
            time.sleep(0.04)
    print(message)

shake_text("CRITICAL HIT! You took 24 damage!")
print("[red]You stumble backward, regaining your footing.[/red]")
