import time
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

def generate_game_screen(turn: int, hp: int) -> Panel:
    """Helper function to build the current state of the UI."""
    content = Text()
    content.append(f"Turn: {turn}\n", style="bold cyan")
    content.append(f"Player HP: {hp}/100\n", style="green" if hp > 30 else "bold red")
    content.append("\n[Press Ctrl+C to exit]", style="dim")

    return Panel(content, title="[bold yellow]Dungeon Crawler[/bold yellow]", border_style="blue")

# Simulate a game loop
try:
    turn = 1
    hp = 100

    # Initialize Live display (auto_refresh keeps it rendering smoothly)
    with Live(generate_game_screen(turn, hp), refresh_per_second=4, screen=False) as live:
        while turn <= 10:
            time.sleep(1.0) # Simulate waiting for player input or game tick

            # Update game state
            turn += 1
            hp -= 10  # Player takes damage every turn

            # Update the live display with the new state
            live.update(generate_game_screen(turn, hp))

        print("\n[bold red]Game Over![/bold red]")

except KeyboardInterrupt:
    print("\nGame exited.")
