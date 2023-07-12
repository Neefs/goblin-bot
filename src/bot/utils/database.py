from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import asyncpg


load_dotenv(".env")
DB_IP = os.getenv("DB_IP")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_DATABASE = os.getenv("DB_DATABASE")

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes = {}

    @staticmethod
    async def get_pool():
        kwargs = {
            "host": DB_IP,
            "port": 5432,
            "user": DB_USER,
            "password": DB_PWD,
            "loop": asyncio.get_event_loop(),
            "database": DB_DATABASE
        }
        return await asyncpg.create_pool(**kwargs)

    async def cog_load(self) -> None:
        Database.pool= await self.get_pool()
        await self.init_tables()
        await self.cache_prefixes()
        
        return await super().cog_load()

    async def cog_unload(self) -> None:
        await Database.pool.close()
        return await super().cog_unload()

    def format_json(self, record:asyncpg.Record):
        if record is None:
            return None
        return {key: value for (key, value) in dict(record).items()}

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.success(f'{self.__class__.__name__} cog is ready!')




    async def init_tables(self) -> None:
        async with self.pool.acquire() as conn:
            conn:asyncpg.Connection
            #CREATE TABLES HERE
            await conn.execute("CREATE TABLE IF NOT EXISTS prefix(guild_id BIGINT, prefix varchar(6))")

    async def get_prefix(self, guild_id, return_none=False) -> str:
        """
        :params: 
        return_none: if false prefix will be created when no prefix is found
        """
        prefix = self.prefixes.get(guild_id)
        if not prefix:
            if return_none:
                return None
            else:
                await self.add_prefix(guild_id)
                return self.bot.default_prefix
        return prefix
    

    async def add_prefix(self, guild_id, prefix=None) -> None:
        if not prefix:
            prefix = self.bot.default_prefix
        if self.prefixes.get(guild_id):
            self.bot.logger.danger(f"WHY THE FUCK {guild_id} TRYING TO HAVE 2 PREFIXES")
            return None
        async with self.pool.acquire() as conn:
            conn:asyncpg.Connection
            await conn.execute("INSERT INTO prefix(guild_id, prefix) VALUES ($1, $2)", guild_id, prefix)
            self.prefixes[guild_id] = prefix

    async def update_prefix(self, guild_id, prefix):
        async with self.pool.acquire() as conn:
            conn:asyncpg.Connection
            await conn.execute("UPDATE prefix SET prefix = $1 WHERE guild_id = $2", prefix, guild_id)
            self.prefixes[guild_id] = prefix

    async def cache_prefixes(self):
        async with self.pool.acquire() as conn:
            conn:asyncpg.Connection
            data = self.format_json(await conn.fetch("SELECT * FROM prefix"))
            self.prefixes = data


            
            


        



async def setup(bot):
    db = Database(bot)
    bot.db = db
    await bot.add_cog(db)
