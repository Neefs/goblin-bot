from discord.ext import commands
import os
import jishaku

class TicketBot(commands.AutoShardedBot):
    def __init__(self, **options):
        self.default_prefix = options.get("prefix", ".")
        super().__init__(command_prefix=self.get_prefix, **options)

        self.ignore_extensions = [

        ]

        if not os.path.exists("extensions"):
            os.mkdir("extensions")
        
        self.extensions_path = [
            "jishaku",
            "utils.database",
            *[
                f"extensions.{ext[:-3]}"
                for ext in os.listdir("extensions")
                if ext.endswith(".py")
                and ext not in self.ignore_extensions
            ]
        ]

    async def get_prefix(self, message):
        return self.default_prefix
    
    async def on_ready(self):
        print("Logged in")