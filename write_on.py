import time

from rich.console import Console


#Writes text char by char on screen
def write_on(text: str, speed: float, color):
    console = Console()
    for char in text:
        console.print(char, end="", style=color)
        time.sleep(speed)
    console.print()
    time.sleep(speed * 8)

#Writes text word by word on screen
def write_on_by_word(text: str, speed: float, color):
    console = Console()
    char_count: int = 0
    for char in text:
        if char != " ":
            console.print(char, end="",style=color)
            char_count += 1
        else:
            console.print(char, end="", style=color)
            relative_sleep_time = speed * (char_count * 1.5) # calculates the delay of next word
            time.sleep(relative_sleep_time)
            char_count = 0
    time.sleep(speed * 5)

    console.print()
    time.sleep(speed * 8)
