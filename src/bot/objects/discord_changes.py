from typing import Any
import discord
import traceback as tb

class Embed(discord.Embed):
    _color = 0xFFC0CB
    bot = None
    def __init__(self, *args, **kwargs):
        if Embed.bot:
            self.set_footer(text="Made by glidin",
                            icon_url=Embed.bot.user.display_avatar.url)
        else:
            self.set_footer(text="Made by glidin")
        self.timestamp = discord.utils.utcnow()
        super().__init__(*args, **kwargs)
        if self.color is None:
            self.color = self._color

class View(discord.ui.View):
    @staticmethod
    async def _respond_with_check(
        interaction: discord.Interaction, embed: discord.Embed, ephemeral: bool = True
    ) -> None:
        try:
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        except (discord.InteractionResponded, discord.errors.HTTPException):
            try:
                await interaction.followup.send(embed=embed)
            except:
                await interaction.channel.send(embed=embed)
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item[Any]) -> None:
        bot = interaction.client
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

    