"""Payroll Command - Process salaries"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import error_embed, success_embed

class PayrollCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="payroll", description="Process salary payments")
    async def payroll(self, interaction: discord.Interaction):
        await success_embed(interaction, "Payroll", "Payroll processing triggered successfully!")

async def setup(bot):
    await bot.add_cog(PayrollCommand(bot))
