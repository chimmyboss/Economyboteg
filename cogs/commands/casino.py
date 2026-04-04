"""Casino Command - Play games"""
import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import success_embed
import random

class CasinoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="casino", description="Play casino games")
    @app_commands.describe(game="slots, coinflip, or dice", amount="Amount to bet")
    async def casino(self, interaction: discord.Interaction, game: str, amount: float):
        if game.lower() == "coinflip":
            result = "Heads" if random.random() > 0.5 else "Tails"
            await success_embed(interaction, "Coin Flip", f"Result: **{result}**")
        elif game.lower() == "dice":
            roll = random.randint(1, 6)
            await success_embed(interaction, "Dice Roll", f"You rolled: **{roll}**")
        elif game.lower() == "slots":
            slots = [random.choice(['🍒', '🍓', '🍋', '🍌', '🎰']) for _ in range(3)]
            await success_embed(interaction, "Slots", f"Reels: {' | '.join(slots)}")
        else:
            await interaction.response.send_message("Unknown game!")

async def setup(bot):
    await bot.add_cog(CasinoCommand(bot))
