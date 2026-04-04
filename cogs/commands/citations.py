"""Citations Command - Issue citations/fines"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import error_embed, success_embed

class CitationsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="citations", description="Issue a citation/fine")
    @app_commands.describe(user="User to cite", amount="Fine amount", reason="Reason")
    async def citations(self, interaction: discord.Interaction, user: discord.User, amount: float, reason: str):
        if amount <= 0:
            await error_embed(interaction, "Amount must be positive!")
            return
        await success_embed(interaction, "Citation Issued", f"✅ Fined {user.mention} ${amount:,.2f} for: {reason}")

async def setup(bot):
    await bot.add_cog(CitationsCommand(bot))
