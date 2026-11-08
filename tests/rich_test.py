from rich import print
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

console = Console()

table = Table(title="Player Inventory")
table.add_column("Item", style="cyan", no_wrap=True)
table.add_column("Qty", style="magenta")
table.add_column("Value", justify="right", style="green")

table.add_row("Iron Sword", "1", "15 gold")
table.add_row("Health Potion", "5", "50 gold")

console.print(table)


console.print(Panel("[bold yellow]A dark presence looms ahead...[/bold yellow]", title="Combat Log", style="red"))



print("[bold red]Danger![/bold red] Something went wrong.")
print("[italic green]Success![/italic green] Mission complete.")
print("[underline cyan]Location:[/underline cyan] Room 402")


layout = Layout()

layout.split_row(
    Layout(Panel("Game Map Window"), name="left"),
    Layout(Panel("Stats & Info"), name="right")
)

console.print(layout)
