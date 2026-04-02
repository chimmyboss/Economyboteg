"""
Embed Utilities - Helper functions for creating Discord embeds
Equivalent to utils/embedUtil.js and utils/embedActionUtil.js
"""

import discord
from discord import Embed, Color
from typing import Optional, List


async def error_embed(
    interaction: discord.Interaction,
    message: str,
    ephemeral: bool = False,
    delete_after: Optional[float] = None
) -> None:
    """Send an error embed response."""
    embed = Embed(
        title="❌ Error",
        description=message,
        color=Color.red()
    )
    embed.set_footer(
        text=interaction.guild.name if interaction.guild else "Error",
        icon_url=interaction.guild.icon.url if interaction.guild and interaction.guild.icon else None
    )
    
    await interaction.response.send_message(
        embed=embed,
        ephemeral=ephemeral,
        delete_after=delete_after
    )


async def success_embed(
    interaction: discord.Interaction,
    title: str,
    message: str,
    ephemeral: bool = False,
    delete_after: Optional[float] = None
) -> None:
    """Send a success embed response."""
    embed = Embed(
        title=f"✅ {title}",
        description=message,
        color=Color.green()
    )
    embed.set_footer(
        text=interaction.guild.name if interaction.guild else "Success",
        icon_url=interaction.guild.icon.url if interaction.guild and interaction.guild.icon else None
    )
    
    await interaction.response.send_message(
        embed=embed,
        ephemeral=ephemeral,
        delete_after=delete_after
    )


async def info_embed(
    interaction: discord.Interaction,
    title: str,
    message: str,
    fields: Optional[List[tuple]] = None,
    ephemeral: bool = False
) -> None:
    """Send an info embed response with optional fields."""
    embed = Embed(
        title=f"ℹ️ {title}",
        description=message,
        color=Color.blue()
    )
    
    if fields:
        for field_name, field_value in fields:
            embed.add_field(name=field_name, value=field_value, inline=False)
    
    embed.set_footer(
        text=interaction.guild.name if interaction.guild else "Info",
        icon_url=interaction.guild.icon.url if interaction.guild and interaction.guild.icon else None
    )
    
    await interaction.response.send_message(
        embed=embed,
        ephemeral=ephemeral
    )


def create_paginated_embed(
    title: str,
    items: List[str],
    items_per_page: int = 10,
    color: Color = Color.blue()
) -> List[Embed]:
    """Create paginated embeds from a list of items."""
    pages = []
    
    for i in range(0, len(items), items_per_page):
        page_items = items[i:i + items_per_page]
        embed = Embed(
            title=title,
            description="\n".join(page_items),
            color=color
        )
        embed.set_footer(text=f"Page {len(pages) + 1}")
        pages.append(embed)
    
    return pages if pages else [
        Embed(
            title=title,
            description="No items to display",
            color=color
        )
    ]


def create_leaderboard_embed(
    guild_name: str,
    title: str,
    entries: List[tuple],
    currency_symbol: str = "$"
) -> Embed:
    """Create a leaderboard embed."""
    embed = Embed(
        title=f"🏆 {title}",
        color=Color.gold()
    )
    
    if not entries:
        embed.description = "No entries to display"
        return embed
    
    leaderboard_text = ""
    for rank, (name, value) in enumerate(entries, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
        leaderboard_text += f"{medal} **{name}** - {currency_symbol}{value:,.2f}\n"
    
    embed.description = leaderboard_text
    embed.set_footer(text=f"{guild_name} Economy System")
    
    return embed


def create_transaction_embed(
    transaction_type: str,
    amount: float,
    account_name: str,
    new_balance: float,
    currency_symbol: str = "$"
) -> Embed:
    """Create a transaction confirmation embed."""
    embed = Embed(
        title=f"Transaction Processed",
        color=Color.green()
    )
    
    embed.add_field(name="Type", value=transaction_type.title(), inline=True)
    embed.add_field(name="Amount", value=f"{currency_symbol}{amount:,.2f}", inline=True)
    embed.add_field(name="Account", value=account_name, inline=False)
    embed.add_field(name="New Balance", value=f"{currency_symbol}{new_balance:,.2f}", inline=False)
    
    return embed


def create_account_embed(
    member: discord.Member,
    account_type: str,
    balance: float,
    currency_symbol: str = "$"
) -> Embed:
    """Create an account details embed."""
    embed = Embed(
        title=f"{member.display_name}'s Balance",
        description="Here is the information that you requested. Use it wisely!",
        color=Color.green()
    )
    
    embed.add_field(
        name="Account Type",
        value=account_type.title(),
        inline=False
    )
    embed.add_field(
        name="Balance",
        value=f"{currency_symbol}{balance:,.2f}",
        inline=False
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.set_footer(text="Economy System")
    
    return embed
