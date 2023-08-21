from discord.ext import commands
from bot.objects.bot import GoblinBot
from typing import Optional, Literal
import discord
from bot.objects.discord_changes import Embed


class Owner(commands.Cog):
    def __init__(self, bot: GoblinBot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author):
            return True
        raise commands.NotOwner("You need to be an owner to run this command.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"✅ {self.__class__.__name__} is ready!")

    @commands.group(invoke_without_command=True, hidden=True)
    @commands.guild_only()
    async def sync(self, ctx: commands.Context, guild_id: Optional[int], copy: bool = False) -> None:
        """Syncs the slash commands with the given guild"""

        if guild_id:
            guild = discord.Object(id=guild_id)
        else:
            guild = ctx.guild

        if copy:
            self.bot.tree.copy_global_to(guild=guild)

        commands = await self.bot.tree.sync(guild=guild)
        await ctx.send(f'Successfully synced {len(commands)} commands')

    @sync.command(name='global')
    async def sync_global(self, ctx: commands.Context):
        """Syncs the commands globally"""

        commands = await self.bot.tree.sync(guild=None)
        await ctx.send(f'Successfully synced {len(commands)} commands')


    @commands.command(hidden=True)
    async def load(self, ctx:commands.Context, *, module:str):
        """Loads a module"""
        module = "bot." + module
        try:
            await self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await self.bot.logger.error(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"\n📥`{module}`")
            await self.bot.logger.info(f"{module} loaded")
    
    @commands.command(hidden=True)
    async def unload(self, ctx:commands.Context, *, module: str):
        """Unloads a module"""
        module = "bot." + module
        try:
            await self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await self.bot.logger.error(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"\n📤`{module}`") 
            await self.bot.logger.info(f"{module} unloaded")
                  

    @commands.command(name="reload", hidden=True)
    async def _reload(self, ctx:commands.Context, *, module: str):
        """Reloads a module"""
        module = "bot." + module
        try:
            await self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await self.bot.logger.error(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"\n🔁`{module}`")
            await self.bot.logger.info(f"{module} reloaded")    
        



async def setup(bot):
    await bot.add_cog(Owner(bot))
