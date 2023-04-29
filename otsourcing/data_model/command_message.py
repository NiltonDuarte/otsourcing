from dataclasses import dataclass
from enum import Enum, auto


class CommandType(Enum):
    STRING_MESSAGE = auto()
    TOGGLE_ATK_MESSAGE = auto()
    TOGGLE_PAUSE_MESSAGE = auto()


@dataclass
class CommandMessage:
    app: str


@dataclass
class StringMessage(CommandMessage):
    message: str
    type = CommandType.STRING_MESSAGE

    def __str__(self):
        return f"{self.app}: {self.message}"


@dataclass
class ToggleAtkMessage(CommandMessage):
    toggle_state: bool
    type = CommandType.TOGGLE_ATK_MESSAGE

    def __str__(self):
        if self.toggle_state:
            msg = f"{self.app}: Attack Enabled"
        else:
            msg = f"{self.app}: Attack Disabled"
        return msg


@dataclass
class TogglePauseMessage(CommandMessage):
    toggle_state: bool
    type = CommandType.TOGGLE_PAUSE_MESSAGE

    def __str__(self):
        if self.toggle_state:
            msg = f"{self.app}: Resumed"
        else:
            msg = f"{self.app}: Paused"
        return msg
