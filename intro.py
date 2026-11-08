from inquirer_textual import prompts

from constants import TEXT_SPEED_FAST, TEXT_SPEED_MEDIUM, TEXT_SPEED_SLOW
from write_on import write_on, write_on_by_word


def intro_sequence():
    text1 = "You wake up feeling like shit..."
    text2 = "Your muscles are sore and your brain is fuzzy.."
    text3 = "What the fuck just happened?"
    text4 = "The floor seems like the coldest thing you've ever felt. You get up, look around and see a bare concrete room. Behind you is a black metallic door with no handle. The door seems strangely clean and out of place."
    text5 = "As you turn back to face the room, your eyes get more used to the darkness. You see details you haven't before"
    text6 = "BLOOD"
    text7 = "There are blood stains everywhere. On the floor. On walls. Even on the ceiling."
    text8 = "As your eyes pan around the ceiling they get caught up by a dark place on the far end of the room."
    text9 = "STAIRS"
    text10 = "There are stairs on the other side of the room. That has to be your way out."

    write_on(text1, TEXT_SPEED_MEDIUM, "italic")
    write_on(text2, TEXT_SPEED_MEDIUM, "italic")
    print()
    write_on_by_word(text3, TEXT_SPEED_SLOW, "bold red")
    print()
    write_on(text4, TEXT_SPEED_MEDIUM, "italic")
    write_on(text5, TEXT_SPEED_MEDIUM, "italic")
    print()
    write_on_by_word(text6, TEXT_SPEED_SLOW, "bold italic red")
    print()
    write_on(text7, TEXT_SPEED_MEDIUM, "italic")
    write_on(text8, TEXT_SPEED_MEDIUM, "italic")
    print()
    write_on_by_word(text9, TEXT_SPEED_SLOW, "bold")
    print()
    write_on(text10, TEXT_SPEED_MEDIUM, "italic")
    print()
    prompts.wait_for_key("Press Enter to continue...", key='enter')
