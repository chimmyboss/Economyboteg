"""Treasury Command - Treasury/government operations"""
import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData

class TreasuryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="treasury", description="View server treasury")
    async def treasury(self, interaction: discord.Interaction):
        if not interaction.guild:
            return
        treasury = await RetrieveData.treasury(str(interaction.guild_id))
        embed = discord.Embed(title="💰 Server Treasury", color=discord.Color.gold())
        embed.add_field(name="Balance", value=f"${float(treasury['balance']) if treasury else 0:,.2f}", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(TreasuryCommand(bot))
