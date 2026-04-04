"""Details Command - User details"""
import discord
from discord.ext import commands
from discord import app_commands
from services.headquarters import RetrieveData
from utils.embeds import error_embed

class DetailsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="details", description="View detailed user information")
    @app_commands.describe(user="User to check")
    async def details(self, interaction: discord.Interaction, user: discord.User = None):
        if not interaction.guild:
            await error_embed(interaction, "Server only!")
            return
        user = user or interaction.user
        try:
            member = await interaction.guild.fetch_member(user.id)
        except:
            await error_embed(interaction, "User not found!")
            return
        accounts = await RetrieveData.user_basic_accounts(interaction, member)
        embed = discord.Embed(title=f"📋 Details - {user.name}", color=discord.Color.blue())
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Registered", value="Yes" if accounts else "No", inline=False)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(DetailsCommand(bot))
