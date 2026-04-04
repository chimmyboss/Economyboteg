"""Leaderboard Command - Top earners"""
import discord
from discord.ext import commands
from discord import app_commands

class LeaderboardCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="leaderboard", description="View top earners")
    async def leaderboard(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
        embed.description = "No data available yet."
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LeaderboardCommand(bot))
