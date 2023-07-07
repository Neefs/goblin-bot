import logging
import os
from typing import List, Union
from discord.ext import commands
from discord.message import Message
from bot.utils.database import Database
import discord
from bot.objects.discord_changes import Embed
import jishaku
import aiohttp
import traceback as tb
import json

class TicketBot(commands.AutoShardedBot):
    def __init__(self, **options):
        self.default_prefix = options.get("prefix", ".")
        super().__init__(self.get_prefix, **options)
        self.db:Database =None
        self.session:aiohttp.ClientSession = None


        self.ignore_extensions = [
        ]
        if not os.path.exists("bot/extensions"):
            os.mkdir("bot/extensions")

        self.extensions_path = [
            "jishaku",
            "bot.utils.database",
            *[
                f"bot.extensions.{ext[:-3]}"
                for ext in os.listdir("bot/extensions")
                if ext.endswith('.py') 
                and ext not in self.ignore_extensions
            ]
        ]

    class Const:
        test_guild = 738060171519197294

    
    
    async def setup_hook(self):
        await self.load_extension("bot.utils.logger")
        self.logger: logging.Logger = self.get_cog("Logger")
        self.logger.setLevel("info")
        self.session = aiohttp.ClientSession()
        for ext in self.extensions_path:
            try:
                await self.load_extension(ext)
            except (
                commands.ExtensionNotFound,
                commands.ExtensionError,
                commands.ExtensionFailed,
            ) as e:
                self.logger.error(f"Failed to load extension '{ext}'. Skipping... {e}")

        self.logger.info("Extensions loaded")
        self.tree.copy_global_to(guild=discord.Object(self.Const.test_guild))
        
        self.logger.debug("")
        self.logger.debug("===== (REBOOT) =====")
        self.logger.debug("")
        self.logger.success("Client class has been initialized")

    async def close(self):
        await self.session.close()
        await super().close()
    
    async def get_prefix(self, message: Message):
        prefix = await self.db.get_prefix(message.guild.id)
        if not prefix:
            await self.db.add_prefix(message.guild.id)
            return self.default_prefix
        print(prefix)
        return prefix

    async def on_ready(self):
        self.logger.success(f"Logged on as {self.user}")

    async def on_command_error(self, ctx:commands.Context, error):
        ignored = (commands.CommandNotFound,)
        read_args = (commands.NotOwner,)
        if isinstance(error, read_args):
            e = Embed(title="Error", description=f"Error: `{error.args[0]}`")
            await ctx.send(embed=e)
            return
        elif isinstance(error, ignored):
            return
            
        else:
            e = Embed(
                title="Error", description=f"There has been an error:"
            )
            traceback = "".join(
                tb.format_exception(type(error), error, error.__traceback__)
            )
            self.logger.error(traceback)
            link = await self.post_code(traceback)
            if len(traceback) >= 2000:
                traceback = f"Error too long use the link provided below."
            e.description += f"\n```py\n{traceback}```\nError also located here: {link}"

            await ctx.send(embed=e)

            


    async def post_code(self, code: str) -> str:
        header = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GIT_KEY')}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        content = json.dumps({
            "public":False,
            "files":{"code.py":{"content":code}}
            })
        
        posted = await self.session.post("https://api.github.com/gists", headers=header, data=content)
        data = await posted.json()
        if posted.status != 201:
            self.logger.critical(f"Could not post code got a code: {posted.status}.\nJson:\n{data}")     
            return f"Error code {posted.status}. Check error logs for more info. "
        link = data["html_url"]
        self.logger.info(f"New gist created. Link: {link}")
        return link