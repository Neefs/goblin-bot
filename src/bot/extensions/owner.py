from discord.ext import commands
from bot.objects.bot import TicketBot
from typing import (Optional, Literal)
import discord
from bot.objects.discord_changes import Embed


class Owner(commands.Cog):
    def __init__(self, bot:TicketBot):
        self.bot = bot

    async def cog_check(self, ctx:commands.Context):
        if await self.bot.is_owner(ctx.author):
            return True
        raise commands.NotOwner("You need to be an owner to run this command.")
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f'✅ {self.__class__.__name__} is ready!')

    @commands.command(name="synccommands", aliases=["synccommand", "sync", "sc"])
    async def sync_commands(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~"]] = None,
    ):
        """Syncs all application commands
        Usage:
        '-sync' | Synchronizes all guilds
        '-sync ~' | Synchronizes current guild
        '-sync id_1, id_2' | Synchronizes specified guilds by id
        :param: guilds: The guilds to sync the command tree to
        :param: spec: Sync to current guild if spec == ~

        :returns: ABSOLUTELY FUCKING NOTHING
        """
        # Credit to Mooshi#6669 for the code revision

        try:
            await ctx.message.delete()
        except:
            pass

        class ConfirmSyncView(discord.ui.View):
            def __init__(self, bot, msg=None):
                self.bot = bot
                self.msg = msg
                super().__init__(timeout=180)

            async def on_timeout(self) -> None:
                try:
                    await self.msg.delete()
                except:
                    pass

            async def interaction_check(self, interaction: discord.Interaction) -> bool:
                return interaction.user == ctx.author

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirm_button(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ):
                if not guilds:
                    if spec == "~":
                        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
                    else:
                        fmt = await ctx.bot.tree.sync()
                    await interaction.response.send_message(
                        embed=Embed(
                            title="Commands Synced",
                            description=f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}",
                        ),
                        ephemeral=True,
                    )
                    self.bot.active_commands = fmt
                    return

                fmt = 0  # what?
                for guild in guilds:
                    try:
                        await ctx.bot.tree.sync(guild=guild)
                    except discord.HTTPException:
                        pass
                    else:
                        fmt += 1

                await interaction.response.send_message(
                    embed=Embed(
                        title="Commands Synced",
                        description=f"Synced the tree to {fmt}/{len(guilds)} guilds.",
                    ),
                    ephemeral=True,
                )

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
            async def cancel_button(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ):
                await interaction.response.send_message(
                    embed=Embed(
                        title="Cancelled",
                        color=0xFF0000,
                        description="Cancelled application commands sync.",
                    ),
                    ephemeral=True,
                )

        view = ConfirmSyncView(self.bot)
        view.msg = await ctx.send("Are you sure", view=view)




async def setup(bot):
    await bot.add_cog(Owner(bot))