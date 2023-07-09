import inspect
from datetime import datetime
import os
from discord.ext import commands

from bot.utils.TextFormat import TextFormat


class Logger(commands.Cog):
    r"""Types
    -------
    info
    warning
    error
    success
    emergency
    alert
    notice
    critical
    debug"""

    level = "debug"
    levels = {
        "emergency": 1,
        "critical": 2,
        "error": 3,
        "alert": 4,
        "warning": 5,
        "notice": 6,
        "success": 7,
        "info": 8,
        "debug": 9,
    }

    @staticmethod
    def log(log_type, content):
        """Logs something to console."""
        date_time = datetime.now()
        if log_type.lower() == "info":
            color = TextFormat.blue
        elif log_type.lower() == "warning":
            color = TextFormat.yellow
        elif log_type.lower() == "error":
            color = TextFormat.red
        elif log_type.lower() == "success":
            color = TextFormat.green
        elif log_type.lower() == "emergency":
            color = TextFormat.gold
        elif log_type.lower() == "alert":
            color = TextFormat.purple
        elif log_type.lower() == "notice":
            color = TextFormat.aqua
        elif log_type.lower() == "critical":
            color = TextFormat.darkRed
        elif log_type.lower() == "debug":
            color = TextFormat.gray
        else:
            return
        lvl = Logger.levels[Logger.level]
        if Logger.levels[log_type.lower()] <= lvl:
            print(
                f"{color}[{log_type.upper()}: {date_time.strftime('%H:%M')}]{TextFormat.white} {content}"
            )
        with open("logs/bot.log", "a") as file:
            try:
                file.write(
                    f"[{log_type.upper()}: {date_time.strftime('%H:%M')}] {content}\n"
                )
            except UnicodeEncodeError:
                file.write(
                    f"[{log_type.upper()}: {date_time.strftime('%H:%M')}] {content.encode('utf-8')}\n"
                )

    @classmethod
    def setLevel(cls, level):
        if level not in cls.levels:
            raise TypeError
        cls.level = level

    @staticmethod
    def info(*content):
        """Logs something with type 'INFO'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def warning(*content):
        """Logs something with type 'WARNING'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def error(*content):
        """Logs something with type 'ERROR'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def success(*content):
        """Logs something with type 'SUCCESS'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def emergency(*content):
        """Logs something with type 'EMERGENCY'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def alert(*content):
        """Logs something with type 'ALERT'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def notice(*content):
        """Logs something with type 'NOTICE'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def critical(*content):
        """Logs something with type 'CRITICAL'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def debug(*content):
        """Logs something with type 'DEBUG'."""
        Logger.log(inspect.stack()[0][3], " ".join([str(c) for c in content]))

    @staticmethod
    def wipe(type_):
        """Wipes log files."""
        if type_ == "logs":
            file = "logs/bot.log"
        elif type_ == "error":
            file = "logs/error.log"
        elif type_ == "discord":
            file = "logs/discord.log"
        else:
            with open("logs/bot.log", "w"):
                pass
            with open("logs/error.log", "w"):
                pass
            with open("logs/discord.log", "w"):
                pass
            return
        with open(file, "w"):
            pass


async def setup(bot):
    if not "logs" in os.listdir():
        os.mkdir("logs")
    await bot.add_cog(Logger())
