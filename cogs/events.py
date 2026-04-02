"""
Event Handlers
Setup Discord bot event handlers
"""

import discord
from discord.ext import commands
from database.models import Guilds, DiscordUsers
from database.server import db_manager
from services.headquarters import UpdateData
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


async def setup_event_handlers(bot: commands.Bot):
    """Setup all event handlers for the bot."""
    
    @bot.event
    async def on_ready():
        """Bot is ready and connected."""
        logger.info(f"Bot logged in as {bot.user}")
        
        try:
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
        
        # Set bot status
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="your economy"
            )
        )
    
    @bot.event
    async def on_guild_join(guild: discord.Guild):
        """Bot joined a new guild."""
        try:
            async with await db_manager.get_session() as session:
                # Check if guild already exists
                stmt = select(Guilds).where(Guilds.IDENT == str(guild.id))
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()
                
                if not existing:
                    new_guild = Guilds(
                        IDENT=str(guild.id),
                        balance=0.0,
                        logging_channel=None
                    )
                    session.add(new_guild)
                    await session.commit()
                    
                    logger.info(f"SERVER-JOINED: Created data for {guild.name}")
                    
                    # Send welcome message
                    if guild.text_channels:
                        welcome_embed = discord.Embed(
                            title=f"Welcome to ECON!",
                            description=f"Thanks for adding the economy bot to **{guild.name}**!\n\nTo get started, use `/help` to see available commands.",
                            color=discord.Color.blue()
                        )
                        try:
                            await guild.text_channels[0].send(embed=welcome_embed)
                        except:
                            pass
        except Exception as e:
            logger.error(f"SERVER-JOINED error: {e}")
    
    @bot.event
    async def on_guild_remove(guild: discord.Guild):
        """Bot left a guild."""
        try:
            await UpdateData.delete_server(str(guild.id))
            logger.warning(f"SERVER-REMOVED: {guild.name} ({guild.id})")
        except Exception as e:
            logger.error(f"SERVER-REMOVED error: {e}")
    
    @bot.event
    async def on_member_join(member: discord.Member):
        """New member joined the guild."""
        try:
            async with await db_manager.get_session() as session:
                # Create discord user if doesn't exist
                stmt = select(DiscordUsers).where(DiscordUsers.IDENT == str(member.id))
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                
                if not user:
                    new_user = DiscordUsers(
                        IDENT=str(member.id),
                        username=str(member)
                    )
                    session.add(new_user)
                    await session.commit()
                
                logger.info(f"MEMBER-JOIN: {member} joined {member.guild.name}")
        except Exception as e:
            logger.error(f"MEMBER-JOIN error: {e}")
    
    @bot.event
    async def on_error(event, *args, **kwargs):
        """Handle bot errors."""
        logger.error(f"Error in {event}:", exc_info=True)


# Event cog for alternative setup
class EventCog(commands.Cog):
    """Event handlers as a cog."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        logger.error(f"Command error in {ctx.command}: {error}")
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have permission to use this command")
        else:
            await ctx.send(f"An error occurred: {str(error)}")


async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(EventCog(bot))
