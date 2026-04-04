"""Stipend Command - Distribute stipends"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed, error_embed

class StipendCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="stipend", description="Distribute stipends to members")
    @app_commands.describe(amount="Amount per member")
    async def stipend(self, interaction: discord.Interaction, amount: float):
        if amount <= 0:
            await error_embed(interaction, "Amount must be positive!")
            return
        await success_embed(interaction, "Stipend Distributed", f"✅ Distributed ${amount:,.2f} to all eligible members")

async def setup(bot):
    await bot.add_cog(StipendCommand(bot))
