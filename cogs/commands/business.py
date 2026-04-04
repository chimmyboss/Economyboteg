"""Business Command - Business management"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed

class BusinessCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="business", description="Manage your business")
    async def business(self, interaction: discord.Interaction):
        embed = discord.Embed(title="💼 Business Management", color=discord.Color.blue())
        embed.description = "You don't own a business yet. Create one to get started!"
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BusinessCommand(bot))
