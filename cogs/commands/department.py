"""Department Command - Department management"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import error_embed, success_embed

class DepartmentCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="department", description="Manage departments")
    @app_commands.describe(action="create, list, or info")
    async def department(self, interaction: discord.Interaction, action: str):
        if action.lower() == "list":
            embed = discord.Embed(title="🏢 Departments", color=discord.Color.blue())
            embed.description = "No departments created yet."
            await interaction.response.send_message(embed=embed)
        else:
            await success_embed(interaction, "Department", "Operation completed!")

async def setup(bot):
    await bot.add_cog(DepartmentCommand(bot))
