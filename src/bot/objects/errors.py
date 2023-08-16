from discord.app_commands import CheckFailure


class NotSetup(CheckFailure):
    def __init__(self, message = "No settings found for this server try running /setup.", *args) -> None:
        super().__init__(message)