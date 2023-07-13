from discord.ext import commands
from discord import app_commands
from bot.objects.discord_changes import Embed
import discord


class Settings(commands.GroupCog, name="settings"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"✅ {self.__class__.__name__} is ready!")

    @app_commands.command(
        name="list", description="Gives you a list of all the settings"
    )
    async def _list(self, interaction: discord.Interaction):
        await interaction.response.send_message("Coming sooooooon")


async def setup(bot):
    await bot.add_cog(Settings(bot))
