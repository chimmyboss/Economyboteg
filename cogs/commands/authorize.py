"""Authorize Command - Grant permissions"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed

class AuthorizeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="authorize", description="Grant permissions to users")
    @app_commands.describe(user="User to authorize", level="Permission level (1-3)")
    async def authorize(self, interaction: discord.Interaction, user: discord.User, level: int):
        if level not in [1, 2, 3]:
            await interaction.response.send_message("Level must be 1, 2, or 3!")
            return
        await success_embed(interaction, "Authorized", f"✅ {user.mention} granted permission level {level}")

async def setup(bot):
    await bot.add_cog(AuthorizeCommand(bot))
