"""
Help Command
Display help for all commands
"""

import discord
from discord.ext import commands
from discord import app_commands


class HelpCommand(commands.Cog):
    """Help command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Show all available commands")
    async def help(self, interaction: discord.Interaction):
        """Help command."""
        embed = discord.Embed(
            title="📖 ECON Bot - Help",
            description="Complete command reference for the economy system",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="💰 Account Commands",
            value="""
/balance - Check your or another user's balance
/register - Register for the economy system
/give @user <amount> - Transfer money to another user
/atm - Bank deposit/withdrawal operations
""",
            inline=False
        )
        
        embed.add_field(
            name="💼 Work & Income",
            value="""
/shift - Track work shifts and hours
/payroll - Process salary payments
/stipend - Distribute stipends to members
""",
            inline=False
        )
        
        embed.add_field(
            name="📊 Information & Reports",
            value="""
/leaderboard - View top earners
/ledger - View transaction history
/inventory - Check your items
/details @user - View detailed user info
""",
            inline=False
        )
        
        embed.add_field(
            name="🏢 Business & Department",
            value="""
/business - Business account operations
/department - Department management
/treasury - Treasury and government operations
/citations - Issue and manage citations/fines
""",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Fun & Games",
            value="""
/casino - Play casino games
""",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Admin Commands",
            value="""
/setup - Initial server setup
/authorize - Grant permissions to users
/set - Configure economy settings
/setlogchannel - Set logging channel
""",
            inline=False
        )
        
        embed.set_footer(text="Use /help to see this message again")
        
        await interaction.response.send_message(embed=embed, ephemeral=False)


async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(HelpCommand(bot))
