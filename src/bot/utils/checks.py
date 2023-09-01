from discord import app_commands
import discord
from bot.objects.errors import NotSetup

def is_ticket_admin():
    async def predicate(interaction:discord.Interaction):
        if not interaction.guild:
            raise app_commands.errors.NoPrivateMessage("This command can only be run in a guild.")
        if interaction.user.guild_permissions.administrator:
            return True
        admin_roles = await interaction.client.db.get_ticket_admin_roles(interaction.guild.id)
        if admin_roles is None:
            raise NotSetup()
        elif admin_roles == []:
            raise NotSetup("No admin roles found.")
        if not any([i for i in interaction.user.roles if i in admin_roles]):
            raise app_commands.errors.MissingAnyRole([i.id for i in admin_roles])
        else:
            return True
        
    return app_commands.check(predicate)
