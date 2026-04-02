"""
Register Command
User registration and account setup
"""

import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData, CreateData
from database.models import AccountType
from utils.embeds import error_embed, success_embed
from decimal import Decimal


class RegisterCommand(commands.Cog):
    """User registration command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name="register",
        description="Register yourself in the economy system"
    )
    async def register(self, interaction: discord.Interaction):
        """Register command."""
        if not interaction.guild:
            await error_embed(
                interaction,
                "This command can only be used in a server!"
            )
            return
        
        try:
            # Check if user already registered
            existing_user = await RetrieveData.user(
                interaction,
                str(interaction.user.id)
            )
            
            if existing_user:
                if existing_user.get("presence") == "ACTIVE":
                    await error_embed(
                        interaction,
                        "You are already registered in the economy system!"
                    )
                    return
                else:
                    # Reactivate inactive user
                    await success_embed(
                        interaction,
                        "Welcome Back",
                        f"Welcome back to **{interaction.guild.name}**! Your account has been reactivated."
                    )
                    return
            
            # Create new accounts for user
            wallet_id = await CreateData.new_account(
                guild_id=str(interaction.guild_id),
                owner_id=str(interaction.user.id),
                account_type=AccountType.PERSONAL_WALLET,
                balance=Decimal("100.00"),
                name=f"{interaction.user.name}'s Wallet"
            )
            
            bank_id = await CreateData.new_account(
                guild_id=str(interaction.guild_id),
                owner_id=str(interaction.user.id),
                account_type=AccountType.PERSONAL_BANK,
                balance=Decimal("0.00"),
                name=f"{interaction.user.name}'s Bank"
            )
            
            if wallet_id and bank_id:
                await success_embed(
                    interaction,
                    "Registration Successful",
                    f"Welcome to the **{interaction.guild.name}** economy system!\n\n"
                    f"✅ Wallet created: $100.00\n"
                    f"✅ Bank account created\n\n"
                    f"Use `/balance` to check your balance and `/help` for available commands!"
                )
            else:
                await error_embed(
                    interaction,
                    "Failed to create accounts. Please try again later."
                )
        
        except Exception as e:
            await error_embed(
                interaction,
                f"An error occurred during registration: {str(e)}"
            )


async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(RegisterCommand(bot))
