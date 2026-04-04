"""Ledger Command - Transaction history"""
import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData
from services.transactions import TransactionService
from utils.embeds import error_embed

class LedgerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ledger", description="View your transaction history")
    async def ledger(self, interaction: discord.Interaction):
        if not interaction.guild:
            await error_embed(interaction, "Server only!")
            return
        accounts = await RetrieveData.user_basic_accounts(interaction, interaction.member)
        if not accounts:
            await error_embed(interaction, "Not registered!")
            return
        transactions = await TransactionService.get_transaction_history(accounts["bank"]["IDENT"], 10)
        embed = discord.Embed(title="📊 Transaction History", color=discord.Color.blue())
        if transactions:
            for tx in transactions[:5]:
                embed.add_field(name=f"{tx['type'].title()}", value=f"${tx['amount']:,.2f} - {tx['description']}", inline=False)
        else:
            embed.description = "No transactions yet."
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LedgerCommand(bot))
