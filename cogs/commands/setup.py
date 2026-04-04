"""Setup Command - Initial server setup"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed

class SetupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setup", description="Setup economy for your server")
    async def setup(self, interaction: discord.Interaction):
        await success_embed(
            interaction, 
            "Server Setup",
            "✅ Economy system initialized!\n\nUse `/help` to see all commands."
        )

async def setup(bot):
    await bot.add_cog(SetupCommand(bot))
