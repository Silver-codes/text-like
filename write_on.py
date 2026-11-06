import time

from rich.console import Console


def write_on(text: str, speed: float, color):
    console = Console()

    for char in text:
        # end="" prevents moving to a new line; style applies Rich formatting
        console.print(char, end="", style=color)
        time.sleep(speed)

    console.print()  # Final newline to finish the line
    time.sleep(speed * 8)

def write_on_by_word(text: str, speed: float, color):
    console = Console()
    char_count: int = 0
    for char in text:
        if char != " ":
            console.print(char, end="",style=color)
            char_count += 1
        # end="" prevents moving to a new line; style applies Rich formatting
        else:
            console.print(char, end="", style=color)
            relative_sleep_time = speed * (char_count * 1.5)
            time.sleep(relative_sleep_time)
            char_count = 0
    time.sleep(speed * 5)

    console.print()  # Final newline to finish the line
    time.sleep(speed * 8)
