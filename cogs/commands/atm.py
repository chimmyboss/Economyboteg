"""ATM Command - Deposit and withdraw from bank"""
import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData
from services.transactions import TransactionService
from utils.embeds import error_embed, success_embed
from decimal import Decimal

class ATMCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="atm", description="Deposit or withdraw from bank")
    @app_commands.describe(action="deposit or withdraw", amount="Amount")
    async def atm(self, interaction: discord.Interaction, action: str, amount: float):
        if not interaction.guild:
            await error_embed(interaction, "Server only!")
            return
        try:
            if action.lower() not in ["deposit", "withdraw"] or amount <= 0:
                await error_embed(interaction, "Invalid action or amount!")
                return
            accounts = await RetrieveData.user_basic_accounts(interaction, interaction.member)
            if not accounts:
                await error_embed(interaction, "Not registered. Use `/register`")
                return
            from_id = accounts["wallet"]["IDENT"] if action.lower() == "deposit" else accounts["bank"]["IDENT"]
            to_id = accounts["bank"]["IDENT"] if action.lower() == "deposit" else accounts["wallet"]["IDENT"]
            success, error_msg = await TransactionService.transfer_money(from_id, to_id, Decimal(str(amount)), f"ATM {action.title()}")
            if success:
                await success_embed(interaction, "Success", f"✅ {action.title()}: ${amount:,.2f}")
            else:
                await error_embed(interaction, error_msg or "Failed!")
        except Exception as e:
            await error_embed(interaction, str(e))

async def setup(bot):
    await bot.add_cog(ATMCommand(bot))
