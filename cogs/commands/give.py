"""
Give Command
Transfer money to another user
"""

import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData
from services.transactions import TransactionService
from utils.embeds import error_embed, success_embed
from decimal import Decimal


class GiveCommand(commands.Cog):
    """Give/transfer money command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="give", description="Transfer money to another user")
    @app_commands.describe(
        user="User to send money to",
        amount="Amount to transfer",
        account_type="From which account (wallet/bank)"
    )
    async def give(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        amount: float,
        account_type: str = "wallet"
    ):
        """Give command."""
        if not interaction.guild:
            await error_embed(interaction, "This command can only be used in a server!")
            return
        
        try:
            # Validate amount
            if amount <= 0:
                await error_embed(interaction, "Amount must be greater than 0!")
                return
            
            if amount > 999999999:
                await error_embed(interaction, "Amount is too large!")
                return
            
            # Check if sender is registered
            sender_accounts = await RetrieveData.user_basic_accounts(
                interaction,
                interaction.member
            )
            
            if not sender_accounts:
                await error_embed(
                    interaction,
                    "You must be registered to use this command. Use `/register` first."
                )
                return
            
            # Check if recipient is registered
            try:
                recipient_member = await interaction.guild.fetch_member(user.id)
            except:
                await error_embed(interaction, "User not found in this server!")
                return
            
            recipient_accounts = await RetrieveData.user_basic_accounts(
                interaction,
                recipient_member
            )
            
            if not recipient_accounts:
                await error_embed(
                    interaction,
                    f"{user.mention} must be registered to receive money."
                )
                return
            
            # Get source account
            source_account = None
            if account_type.lower() == "bank":
                source_account = sender_accounts["bank"]["IDENT"]
            else:
                source_account = sender_accounts["wallet"]["IDENT"]
            
            # Get destination account (always wallet)
            dest_account = recipient_accounts["wallet"]["IDENT"]
            
            # Perform transfer
            success, error_msg = await TransactionService.transfer_money(
                source_account,
                dest_account,
                Decimal(str(amount)),
                f"Transfer from {interaction.user.mention}"
            )
            
            if success:
                await success_embed(
                    interaction,
                    "Transfer Successful",
                    f"✅ Transferred **${amount:,.2f}** to {user.mention}"
                )
            else:
                await error_embed(interaction, error_msg or "Transfer failed!")
        
        except ValueError:
            await error_embed(interaction, "Invalid amount. Please enter a number.")
        except Exception as e:
            await error_embed(interaction, f"An error occurred: {str(e)}")


async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(GiveCommand(bot))
