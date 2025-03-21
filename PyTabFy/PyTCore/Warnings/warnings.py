from enum import Enum
from typing import Dict, Optional


class WarningLevel(Enum):

    INFO:    str = "INFO"
    ERROR:   str = "ERROR"
    WARNING: str = "WARNING"


class WarningPrinter():

    NO_COLOR: str = '\033[0m'
    COLORS: Dict[WarningLevel, str] = {
        WarningLevel.INFO:    '\033[94m', # Blue
        WarningLevel.ERROR:   '\033[91m', # Red
        WarningLevel.WARNING: '\033[93m', # Yellow  
    }

    def __init__(self, warning_level: WarningLevel) -> None:
        self.warning_level = warning_level

    def get_color(self) -> str:
        return self.COLORS.get(self.warning_level)

    def print(self, *, info: str, from_class: str) -> None:
        color = self.get_color()

        print(f"{color}[{from_class}][{self.warning_level.value}] --->{self.NO_COLOR} {info}")


class BaseWarning(WarningPrinter):

    def __init__(self, warning_level: WarningLevel) -> None:
        super().__init__(warning_level)

    def print(self, *, info, from_class) -> None:
        from PyTabFy import global_configs
        
        if not global_configs.disable_warnings:
            return super().print(info=info, from_class=from_class)


class ConfigWarning(BaseWarning):

    def __init__(self, info: str, warning_level: WarningLevel, from_class: Optional[str] = None) -> None:
        super().__init__(warning_level)

        self.print(info=info, from_class=from_class if from_class is not None else __class__.__name__)


class InvalidDataWarning(BaseWarning):

    def __init__(self, info: str, warning_level: WarningLevel, from_class: Optional[str] = None) -> None:
        super().__init__(warning_level)

        self.print(info=info, from_class=from_class if from_class is not None else __class__.__name__)
