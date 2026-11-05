from inquirer_textual import prompts
from inquirer_textual.common.PromptSettings import PromptSettings
from inquirer_textual.InquirerApp import InquirerApp
from inquirer_textual.widgets.InquirerSelect import InquirerSelect
from rich.console import Console
from rich.panel import Panel

from clear_screen import clear_screen


class NoQuestionApp(InquirerApp):
    CSS = "Prompt { display: none; }"


def select_menu(choices, settings=PromptSettings()):
    app = NoQuestionApp(theme=settings.theme)
    app.widget = InquirerSelect('', choices, mandatory=settings.mandatory)
    return app.run_with_settings(settings)


def main_menu():
    console = Console()
    console.print(Panel("[bold yellow]Welcome to Text-Like[/bold yellow]", title="Text-like", style="blue"))
    result = select_menu(['Continue', 'Load game', 'Exit'],
                         settings=PromptSettings(mandatory=False))
    if result == "Exit":
        clear_screen()
        return
    elif result == "Continue":  # noqa: SIM114
        clear_screen()
        pass
    elif result == "Load game":
        clear_screen()
        pass
