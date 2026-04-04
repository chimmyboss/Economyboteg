"""Set Command - Configuration settings"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed

class SetCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="set", description="Configure economy settings")
    @app_commands.describe(setting="Setting name", value="Setting value")
    async def set(self, interaction: discord.Interaction, setting: str, value: str):
        await success_embed(interaction, "Setting Updated", f"✅ {setting} set to {value}")

async def setup(bot):
    await bot.add_cog(SetCommand(bot))
