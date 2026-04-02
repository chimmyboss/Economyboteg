"""
Balance Command
Check user's wallet and bank balance
"""

import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData, GuildHQ
from utils.embeds import error_embed, info_embed
from decimal import Decimal


class BalanceCommand(commands.Cog):
    """Balance command cog."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="balance", description="Check your balance or another user's balance")
    @app_commands.describe(user="The user to check the balance of")
    async def balance(
        self,
        interaction: discord.Interaction,
        user: discord.User = None
    ):
        """Check balance command."""
        if not interaction.guild:
            await error_embed(
                interaction,
                "This command can only be used in a server!"
            )
            return
        
        # Get member to check (default to command executor)
        member_to_check = user or interaction.user
        
        try:
            # Fetch user member object
            try:
                member_obj = await interaction.guild.fetch_member(member_to_check.id)
            except:
                member_obj = discord.Object(id=member_to_check.id)
                member_obj.display_name = member_to_check.name
            
            # Retrieve accounts
            accounts = await RetrieveData.user_basic_accounts(
                interaction,
                member_obj
            )
            
            if not accounts or not accounts.get("bank"):
                await error_embed(
                    interaction,
                    f"{member_to_check.mention} does not have any accounts registered to the economy!"
                )
                return
            
            # Format money
            guild_manager = GuildHQ(interaction)
            bank_balance = await guild_manager.format_money(
                Decimal(str(accounts["bank"]["balance"]))
            )
            wallet_balance = await guild_manager.format_money(
                Decimal(str(accounts["wallet"]["balance"]))
            )
            
            # Create embed
            embed = discord.Embed(
                title=f"{member_to_check.display_name}'s Balance",
                description="Here is the information that you requested. Use it wisely!",
                color=discord.Color.green()
            )
            
            embed.add_field(name="💳 Bank", value=bank_balance, inline=True)
            embed.add_field(name="💰 Wallet", value=wallet_balance, inline=True)
            
            # Total balance
            total = Decimal(str(accounts["bank"]["balance"])) + Decimal(str(accounts["wallet"]["balance"]))
            total_formatted = await guild_manager.format_money(total)
            embed.add_field(name="📊 Total", value=total_formatted, inline=False)
            
            embed.set_color(discord.Color.green())
            embed.set_footer(
                text=f"{interaction.guild.name} Economy System",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            
            # Check for premium
            is_premium = await guild_manager.get_premium_status()
            
            await interaction.response.send_message(embed=embed, ephemeral=not is_premium)
        
        except Exception as e:
            await error_embed(
                interaction,
                f"An error occurred while retrieving balance: {str(e)}"
            )


async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(BalanceCommand(bot))
