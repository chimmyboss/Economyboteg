"""
Ping Command
Simple ping/pong command for testing
"""

import discord
from discord.ext import commands
from discord import app_commands


class PingCommand(commands.Cog):
    """Simple ping command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Replies with Pong!")
    async def ping(self, interaction: discord.Interaction):
        """Ping command."""
        await interaction.response.send_message(
            f"Pong! Latency: {self.bot.latency * 1000:.2f}ms"
        )


async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(PingCommand(bot))
