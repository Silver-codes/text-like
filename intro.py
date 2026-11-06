from constants import TEXT_SPEED_FAST, TEXT_SPEED_MEDIUM, TEXT_SPEED_SLOW
from write_on import write_on, write_on_by_word


def intro_sequence():
    text1 = "You wake up feeling like shit..."
    text2 = "Your muscles are sore and your brain is fuzzy.."
    text3 = "What the fuck just happened?"

    write_on(text1, TEXT_SPEED_MEDIUM, "bold red")
    write_on(text2, TEXT_SPEED_MEDIUM, "bold red")
    write_on_by_word(text3, TEXT_SPEED_SLOW, "bold red")
