from discord import app_commands, Embed
import discord
import traceback as tb

from discord.interactions import Interaction
from bot.objects.discord_changes import Embed

class CommandTree(app_commands.CommandTree):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(bot)

    @staticmethod
    async def _respond_with_check(
        interaction: Interaction, embed: discord.Embed, ephemeral: bool = True
    ) -> None:
        try:
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        except (discord.InteractionResponded, discord.errors.HTTPException):
            try:
                await interaction.followup.send(embed=embed)
            except:
                await interaction.channel.send(embed=embed)

    async def interaction_check(self, interaction:Interaction):
        if not interaction.guild:
            raise app_commands.NoPrivateMessage("Commands are only available in guilds.")
        return True
    
    async def on_error(self, interaction: Interaction, error: app_commands.AppCommandError) -> None:
        bot = interaction.client
        ignored = ()
        read_args = (app_commands.NoPrivateMessage)
        if isinstance(error, ignored):
            return
        elif isinstance(error, read_args):
            embed = Embed(
                title="Error",
                description="Error: `{0}`".format(error.args[0]),
            )
        else:
            embed = Embed(
                title="Error", description=f"There has been an error:"
            )
            traceback = "".join(
                tb.format_exception(type(error), error, error.__traceback__)
            )
            bot.logger.error(traceback)
            link = await bot.post_code(traceback)
            if len(traceback) >= 2000:
                traceback = f"Error too long use the link provided below."
            embed.description += f"\n```py\n{traceback}```\nError also located here: {link}"
        await self._respond_with_check(interaction, embed)

