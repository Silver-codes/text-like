import os
import sys
import time
from contextlib import contextmanager

from rich.console import Console

console = Console()

if os.name == "nt":  # Windows
    import msvcrt

    def key_pressed() -> bool:
        if msvcrt.kbhit():
            msvcrt.getwch()  # consume the key
            return True
        return False

    @contextmanager
    def instant_keys():
        try:
            yield
        finally:
            while msvcrt.kbhit():  # discard leftover keypresses
                msvcrt.getwch()

else:  # macOS / Linux
    import select
    import termios
    import tty

    def key_pressed() -> bool:
        if select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.read(1)  # consume the key
            return True
        return False

    @contextmanager
    def instant_keys():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)  # keys arrive immediately, without Enter
            yield
        finally:
            termios.tcflush(fd, termios.TCIFLUSH)  # discard leftover keypresses
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def flush_input(): #Discard any keys pressed but not yet read
    if os.name == "nt":
        while msvcrt.kbhit():
            msvcrt.getwch()
    else:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

#Writes text char by char on screen
def write_on(text: str, speed: float, color):
    with instant_keys():
        for i, char in enumerate(text):
            if key_pressed():
                console.print(text[i:], end="", style=color)  # print the rest at once
                time.sleep(speed * 3) # makes the sleep longer if writing on is skipped
                break
            console.print(char, end="", style=color)
            time.sleep(speed)
    console.print()
    time.sleep(speed * 8)
    flush_input()

#Writes text word by word on screen
def write_on_by_word(text: str, speed: float, color):
    with instant_keys():
        char_count = 0
        for i, char in enumerate(text):
            console.print(char, end="", style=color)
            if char != " ":
                char_count += 1
                continue
            if key_pressed():
                console.print(text[i + 1:], end="", style=color)  # rest at once
                time.sleep(speed * 3) # makes the sleep longer if writing on is skipped
                break
            time.sleep(speed * char_count * 1.5)  # delay before the next word
            char_count = 0
        else:
            time.sleep(speed * 5)  # only runs if the text wasn't skipped
    console.print()
    time.sleep(speed * 8)
    flush_input()
