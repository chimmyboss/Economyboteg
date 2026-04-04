"""Inventory Command - Check items"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import error_embed

class InventoryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="inventory", description="Check your inventory")
    async def inventory(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📦 Your Inventory", color=discord.Color.blue())
        embed.description = "Your inventory is currently empty."
        embed.add_field(name="Total Items", value="0", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InventoryCommand(bot))
