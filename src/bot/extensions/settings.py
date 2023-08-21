from discord.ext import commands
from discord import app_commands
from bot.objects.discord_changes import Embed, Group
import discord
from bot.objects.bot import GoblinBot
from bot.utils.checks import is_ticket_admin
from typing import Optional


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
        settings = {
            "support_roles": await self.bot.db.get_ticket_support_roles(interaction.guild.id) or [],
            "admin_roles": await self.bot.db.get_ticket_admin_roles(interaction.guild.id) or [],
            "ticket_category": await self.bot.db.get_ticket_category(interaction.guild.id)
        }
        embed = Embed(title=f"{interaction.guild.name}'s settings")
        embed.add_field(name="Support Roles", value= "None" if settings["support_roles"] == [] else ", ".join([role.mention for role in settings["support_roles"]]), inline=False)
        embed.add_field(name="Admin Roles", value= "None" if settings["admin_roles"] == [] else ", ".join([role.mention for role in settings["admin_roles"]]), inline=False)
        embed.add_field(name="Ticket Category", value=f"<#{settings['ticket_category']}>" if settings["ticket_category"] else "Not set", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @app_commands.command(
        description="Sets ticket category"
    )
    async def ticket_category(self, interaction:discord.Interaction, category:Optional[discord.CategoryChannel]):
        if not category:
            cat = await self.bot.db.get_ticket_category(interaction.guild.id)
            if not cat:
                await interaction.response.send_message("Category not set")
                return
            await interaction.response.send_message(embed=Embed(description=f"Category: <#{category}>"))
            return
        #set ticket category here
            

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
        name="add", description="Adds an admin role"
    )
    async def admin_role_add(self, interaction:discord.Interaction, role:discord.Role):
        roleadded = role.id == (await self.bot.db.add_ticket_admin_roles(interaction.guild.id, role.id))
        if roleadded:
            await interaction.response.send_message(f"{role.mention} added to admin roles", ephemeral=True)
        else:
            await interaction.response.send_message(f"{role.mention} couldn't be added. Is this role already an admin role?", ephemeral=True)


    @admin_role_group.command(
        name="remove", description="Removes an admin role"
    )
    async def admin_role_remove(self, interaction:discord.Interaction, role:discord.Role):
        roleremoved = await self.bot.db.remove_ticket_support_roles(interaction.guild.id, role.id)
        if roleremoved is None:
            await interaction.response.send_message(f"No settings found. Have you run the setup command yet?", ephemeral=True)
            return
        roleremoved = role.id in roleremoved
        if roleremoved:
            await interaction.response.send_message(f"{role.mention} removed from support roles", ephemeral=True)
        else:
            await interaction.response.send_message(f"{role.mention} couldn't be removed. Is this role a support role?", ephemeral=True)



async def setup(bot):
    await bot.add_cog(Settings(bot))
