from time import sleep

from PyTabFy.Others import build_ascii_art


class GlobalConfigs():
    _instance = None

    def __new__(cls, *args, **kwargs) -> 'GlobalConfigs':
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.__init__()

        return cls._instance


    def __init__(self) -> None:
        self.show_ascii_art_on_init: bool = True
        self.was_ascii_art_shown:    bool = False
        self.disable_warnings:       bool = False


    def _display_ascii_art(self) -> None:
        """A one-time display of the PyTabFy ASCII art"""

        if self.show_ascii_art_on_init and not self.was_ascii_art_shown:
            print('\n')
            for line in build_ascii_art():
                sleep(0.15)
                print(f'   {line}')
            print('\n\n')
            sleep(1)
            self.was_ascii_art_shown = True
