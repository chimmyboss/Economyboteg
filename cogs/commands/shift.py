"""Shift Command - Track work shifts"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import error_embed, success_embed

class ShiftCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="shift", description="Start or end your work shift")
    @app_commands.describe(action="start or end")
    async def shift(self, interaction: discord.Interaction, action: str):
        if action.lower() not in ["start", "end"]:
            await error_embed(interaction, "Action must be 'start' or 'end'!")
            return
        await success_embed(interaction, "Shift", f"✅ Shift {action.title()}ed successfully!")

async def setup(bot):
    await bot.add_cog(ShiftCommand(bot))
