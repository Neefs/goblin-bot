from discord.ext import commands
from discord import app_commands
from bot.objects.discord_changes import Embed, Group
import discord
from bot.objects.bot import GoblinBot
from bot.utils.checks import is_ticket_admin


class Settings(commands.GroupCog, name="settings"):
    def __init__(self, bot: GoblinBot):
        self.bot = bot
        self.settings = [
            "support_roles",
            "admin_roles",
            "ticket_category"
        ]
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"✅ {self.__class__.__name__} is ready!")

    @app_commands.command(
        name="list", description="Gives you a list of all the settings"
    )
    async def _list(self, interaction: discord.Interaction):
        setting_to_command = []
        await interaction.response.send_message("Coming sooooooon")

    support_role_group = Group(name="support_role")
    admin_role_group  = Group(name="admin_role")

    @support_role_group.command(
        name="help", description="Sends help message for this group."
    )
    @is_ticket_admin()
    async def support_role_help(self, interaction:discord.Interaction):
        await interaction.response.send_message("test")

    @support_role_group.command(
        name="add", description="adds a support role"
    )
    async def support_role_add(self, interaction:discord.Interaction, role:discord.Role):
        roleadded = role.id == (await self.bot.db.add_ticket_support_roles(interaction.guild.id, role.id))
        if roleadded:
            await interaction.response.send_message(f"{role.mention} added to support roles", ephemeral=True)
        else:
            await interaction.response.send_message(f"{role.mention} couldn't be added. Is this role already a support role?", ephemeral=True)

    @support_role_group.command(
        name="remove", description="Removes a support role."
    )
    async def support_role_remove(self, interaction:discord.Interaction, role: discord.Role):
        roleremoved = await self.bot.db.remove_ticket_support_roles(interaction.guild.id, role.id)
        if roleremoved is None:
            await interaction.response.send_message(f"No settings found. Have you run the setup command yet?", ephemeral=True)
            return
        roleremoved = role.id in roleremoved
        if roleremoved:
            await interaction.response.send_message(f"{role.mention} removed from support roles", ephemeral=True)
        else:
            await interaction.response.send_message(f"{role.mention} couldn't be removed. Is this role a support role?", ephemeral=True)


    @support_role_group.command(
        name="list", description="lists all the support roles in this server"
    )
    async def support_role_list(self, interaction:discord.Interaction):
        roles = await self.bot.db.get_ticket_support_roles(interaction.guild.id)
        await interaction.response.send_message(embed=Embed(title="Support Roles", description=",".join(role.mention for role in roles) if roles and roles != [] else "None"), ephemeral=True)


    @admin_role_group.command(
        name="help", description="Sends help message for this group."
    )
    async def admin_role_help(self, interaction:discord.Interaction):
        await interaction.response.send_message("test")

    @admin_role_group.command(
        name="add", description="adds a admin role"
    )
    async def admin_role_add(self, interaction:discord.Interaction, role:discord.Role):
        roleadded = role.id == (await self.bot.db.add_ticket_admin_roles(interaction.guild.id, role.id))
        if roleadded:
            await interaction.response.send_message(f"{role.mention} added to admin roles", ephemeral=True)
        else:
            await interaction.response.send_message(f"{role.mention} couldn't be added. Is this role already an admin role?", ephemeral=True)



async def setup(bot):
    await bot.add_cog(Settings(bot))
