"""
ECON Discord Bot - Main Entry Point
Discord.py version (converted from Discord.js)
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from database.server import SQLManager
from cogs.events import setup_event_handlers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize database
db = SQLManager()


async def setup_database():
    """Initialize and authenticate database connection."""
    try:
        await db.authenticate()
        logger.info("Connection established successfully.")
    except Exception as e:
        logger.error(f"Unable to establish connection: {e}")
        raise


async def load_commands():
    """Load all command cogs from the commands directory."""
    commands_path = Path("cogs/commands")
    
    if not commands_path.exists():
        logger.warning(f"Commands directory not found: {commands_path}")
        return
    
    for file in commands_path.glob("*.py"):
        if file.name.startswith("_"):
            continue
        
        cog_name = file.stem
        try:
            await bot.load_extension(f"cogs.commands.{cog_name}")
            logger.info(f"Loaded command: {cog_name}")
        except Exception as e:
            logger.error(f"Failed to load {cog_name}: {e}")


async def setup_bot():
    """Initialize and setup the bot."""
    # Create bot instance with appropriate intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.guild_members = True
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="/", intents=intents)
    
    # Setup database
    await setup_database()
    
    # Load commands
    await load_commands()
    
    # Setup event handlers
    await setup_event_handlers(bot)
    
    return bot


# Premium commands list
PREMIUM_CMDS = ["quick-sell", "set-currency", "set-payroll-tax", "set-sales-tax", "inflate", "deflate"]
SERVER_BYPASS = os.getenv("server_bypass", "").split(", ") if os.getenv("server_bypass") else []


async def main():
    """Main entry point for the bot."""
    global bot
    
    bot = await setup_bot()
    
    @bot.event
    async def on_ready():
        logger.info(f"Bot logged in as {bot.user}")
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="your economy")
        )
    
    # Start the bot
    token = os.getenv("token")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable not set")
    
    await bot.start(token)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
