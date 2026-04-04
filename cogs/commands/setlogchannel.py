"""Setlogchannel Command - Configure logging channel"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed

class SetlogchannelCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setlogchannel", description="Set logging channel")
    @app_commands.describe(channel="Channel for logs")
    async def setlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await success_embed(interaction, "Logging Configured", f"✅ Logs will be sent to {channel.mention}")

async def setup(bot):
    await bot.add_cog(SetlogchannelCommand(bot))
