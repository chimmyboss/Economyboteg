"""
# DISCORD.JS → DISCORD.PY MIGRATION GUIDE

This document provides detailed mappings for converting Discord.js code to Discord.py for the ECON bot.

## TABLE OF CONTENTS
1. Basic Syntax
2. Discord API Objects
3. Commands and Interactions
4. Database Operations
5. Event Handling
6. Utility Functions
7. Common Patterns

---

## 1. BASIC SYNTAX

### Imports

#### Discord.js
```javascript
const { Client, Collection, GatewayIntentBits } = require('discord.js');
const fs = require('fs');
const path = require('path');
```

#### Discord.py
```python
import discord
from discord.ext import commands
from pathlib import Path
import logging
```

### Client Initialization

#### Discord.js
```javascript
const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers],
    partials: [Partials.Channel]
});

client.commands = new Collection();
```

#### Discord.py
```python
intents = discord.Intents.default()
intents.guilds = True
intents.guild_members = True

bot = commands.Bot(command_prefix="/", intents=intents)
```

---

## 2. DISCORD API OBJECTS

### Interactions

#### Discord.js
```javascript
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand()) return;
    
    const command = client.commands.get(interaction.commandName);
    await command.execute(interaction);
});
```

#### Discord.py
```python
@app_commands.command(name="mycommand")
async def mycommand(interaction: discord.Interaction):
    await interaction.response.send_message("Response")
```

### Embeds

#### Discord.js
```javascript
const embed = new EmbedBuilder()
    .setTitle("Title")
    .setDescription("Description")
    .addFields(
        { name: "Field 1", value: "Value 1" },
        { name: "Field 2", value: "Value 2" }
    )
    .setColor("#0099ff");

await interaction.reply({ embeds: [embed] });
```

#### Discord.py
```python
embed = discord.Embed(
    title="Title",
    description="Description",
    color=discord.Color.blue()
)
embed.add_field(name="Field 1", value="Value 1", inline=False)
embed.add_field(name="Field 2", value="Value 2", inline=False)

await interaction.response.send_message(embed=embed)
```

### Members and Users

#### Discord.js
```javascript
const user = await interaction.guild.members.fetch(userId);
console.log(user.displayName);
console.log(user.id);
```

#### Discord.py
```python
try:
    user = await interaction.guild.fetch_member(user_id)
    print(user.display_name)
    print(user.id)
except discord.NotFound:
    print("User not found")
```

### Role Operations

#### Discord.js
```javascript
const role = await interaction.guild.roles.create({
    name: "Investor",
    permissions: ["ManageMessages"]
});

await member.roles.add(role);
await member.roles.remove(role);
```

#### Discord.py
```python
role = await interaction.guild.create_role(
    name="Investor",
    permissions=discord.Permissions(manage_messages=True)
)

await member.add_roles(role)
await member.remove_roles(role)
```

---

## 3. COMMANDS AND INTERACTIONS

### Slash Command Structure

#### Discord.js
```javascript
const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('balance')
        .setDescription('Check balance')
        .addUserOption(option =>
            option.setName('user')
                .setDescription('User to check')
                .setRequired(false)
        ),
    async execute(interaction) {
        const user = interaction.options.getUser('user') || interaction.user;
        await interaction.reply(`Balance: $100`);
    }
};
```

#### Discord.py
```python
from discord import app_commands
from discord.ext import commands

class BalanceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="balance", description="Check balance")
    @app_commands.describe(user="User to check")
    async def balance(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        await interaction.response.send_message(f"Balance: $100")

async def setup(bot):
    await bot.add_cog(BalanceCommand(bot))
```

### Handling Options

#### Discord.js
```javascript
const amount = interaction.options.getNumber('amount');
const user = interaction.options.getUser('user');
const channel = interaction.options.getChannel('channel');
const role = interaction.options.getRole('role');
```

#### Discord.py
```python
# Define in decorator
@app_commands.describe(
    amount="Amount in dollars",
    user="Target user",
    channel="Target channel",
    role="Target role"
)
async def command(
    self,
    interaction: discord.Interaction,
    amount: float,
    user: discord.User = None,
    channel: discord.TextChannel = None,
    role: discord.Role = None
):
    # Parameters are automatically extracted
    pass
```

### Responding to Interactions

#### Discord.js
```javascript
// Reply
await interaction.reply("Hello!");
await interaction.reply({ embeds: [embed], ephemeral: true });

// Defer
await interaction.deferReply({ ephemeral: true });
await interaction.editReply("Updated");

// Follow-up
await interaction.followUp("Follow up message");
```

#### Discord.py
```python
# Reply
await interaction.response.send_message("Hello!")
await interaction.response.send_message(embed=embed, ephemeral=True)

# Defer
await interaction.response.defer(ephemeral=True)
await interaction.followup.send("Updated")

# Follow-up
await interaction.followup.send("Follow up message")
```

---

## 4. DATABASE OPERATIONS

### Sequelize → SQLAlchemy

#### Sequelize (JavaScript)
```javascript
const user = await User.findOne({
    where: {
        userId: '123',
        guildId: '456'
    }
});

const users = await User.findAll({
    where: { guildId: '456' },
    limit: 10,
    order: [['createdAt', 'DESC']]
});

await user.update({ balance: 100 });
await user.destroy();
```

#### SQLAlchemy (Python)
```python
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

async with session:
    # Find one
    stmt = select(User).where(
        and_(
            User.userId == '123',
            User.guildId == '456'
        )
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    # Find all
    stmt = select(User).where(
        User.guildId == '456'
    ).order_by(
        User.createdAt.desc()
    ).limit(10)
    result = await session.execute(stmt)
    users = result.scalars().all()

    # Update
    user.balance = 100
    await session.commit()

    # Delete
    await session.delete(user)
    await session.commit()
```

### Model Definition

#### Sequelize
```javascript
const User = sequelize.define('User', {
    IDENT: {
        type: DataTypes.UUID,
        primaryKey: true
    },
    guild: {
        type: DataTypes.TEXT,
        allowNull: false,
        references: {
            model: 'Guilds',
            key: 'IDENT'
        }
    },
    balance: {
        type: DataTypes.DECIMAL(20, 2)
    }
});
```

#### SQLAlchemy
```python
from sqlalchemy import Column, String, DECIMAL, ForeignKey

class User(Base):
    __tablename__ = "users"
    
    IDENT = Column(String, primary_key=True)
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    balance = Column(DECIMAL(20, 2))
```

---

## 5. EVENT HANDLING

### Registering Events

#### Discord.js
```javascript
client.on('ready', () => {
    console.log('Bot is ready!');
});

client.on('guildCreate', async (guild) => {
    console.log(`Joined guild: ${guild.name}`);
});

client.on('guildDelete', async (guild) => {
    console.log(`Left guild: ${guild.name}`);
});
```

#### Discord.py
```python
@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_guild_join(guild):
    print(f"Joined guild: {guild.name}")

@bot.event
async def on_guild_remove(guild):
    print(f"Left guild: {guild.name}")
```

### Event in Cogs

#### Discord.js
```javascript
// events/ready.js
module.exports = {
    name: 'ready',
    once: true,
    execute(client) {
        console.log(`Ready as ${client.user.tag}`);
    }
};

// index.js
const eventFiles = fs.readdirSync('./events');
for (const file of eventFiles) {
    const event = require(`./events/${file}`);
    if (event.once) {
        client.once(event.name, (...args) => event.execute(...args));
    } else {
        client.on(event.name, (...args) => event.execute(...args));
    }
}
```

#### Discord.py (Cog)
```python
# cogs/events.py
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ready as {self.bot.user}")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined guild: {guild.name}")

async def setup(bot):
    await bot.add_cog(Events(bot))
```

---

## 6. UTILITY FUNCTIONS

### Formatting Numbers

#### JavaScript
```javascript
function formatMoney(amount, currency = '$') {
    return `${currency}${amount.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })}`;
}
```

#### Python
```python
def format_money(amount: float, currency: str = "$") -> str:
    return f"{currency}{amount:,.2f}"

# Or using locale
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
formatted = f"{currency}{amount:,.2f}"
```

### Error Handling

#### JavaScript
```javascript
try {
    const result = await someAsyncFunction();
} catch (error) {
    console.error('Error:', error);
    await interaction.reply('An error occurred');
}
```

#### Python
```python
import logging

logger = logging.getLogger(__name__)

try:
    result = await some_async_function()
except Exception as e:
    logger.error(f"Error: {e}")
    await interaction.response.send_message("An error occurred")
```

---

## 7. COMMON PATTERNS

### Loading Commands Dynamically

#### Discord.js
```javascript
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath)
    .filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    client.commands.set(command.data.name, command);
}
```

#### Discord.py
```python
from pathlib import Path

async def load_commands(bot):
    cogs_path = Path("cogs/commands")
    
    for cog_file in cogs_path.glob("*.py"):
        if cog_file.name.startswith("_"):
            continue
        
        cog_name = cog_file.stem
        try:
            await bot.load_extension(f"cogs.commands.{cog_name}")
        except Exception as e:
            print(f"Failed to load {cog_name}: {e}")

# In main.py
await load_commands(bot)
```

### Caching Data

#### JavaScript (Keyv)
```javascript
const keyv = new Keyv();

// Set
await keyv.set('user:123', userData, 60000); // 1 minute TTL

// Get
const data = await keyv.get('user:123');

// Delete
await keyv.delete('user:123');
```

#### Python (aioredis)
```python
import aioredis

redis = await aioredis.create_redis_pool('redis://localhost')

# Set
await redis.setex('user:123', 60, json.dumps(userData))

# Get
data = await redis.get('user:123')

# Delete
await redis.delete('user:123')
```

### Pagination

#### Discord.js
```javascript
const embeds = createPaginatedEmbeds(items);
const paginationButtons = new ActionRowBuilder()
    .addComponents(
        new ButtonBuilder().setCustomId('previous'),
        new ButtonBuilder().setCustomId('next')
    );

const response = await interaction.reply({
    embeds: [embeds[0]],
    components: [paginationButtons]
});

const collector = response.createMessageComponentCollector();
```

#### Discord.py
```python
import discord
from discord.ui import View, Button

class PaginationView(View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current = 0
    
    @discord.ui.button(label="Previous")
    async def previous(self, interaction: discord.Interaction, button: Button):
        if self.current > 0:
            self.current -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current])
    
    @discord.ui.button(label="Next")
    async def next(self, interaction: discord.Interaction, button: Button):
        if self.current < len(self.embeds) - 1:
            self.current += 1
            await interaction.response.edit_message(embed=self.embeds[self.current])

# Usage
view = PaginationView(embeds)
await interaction.response.send_message(embed=embeds[0], view=view)
```

---

## QUICK REFERENCE

| Task | Discord.js | Discord.py |
|------|-----------|-----------|
| Send message | `await interaction.reply()` | `await interaction.response.send_message()` |
| Create embed | `new EmbedBuilder()` | `discord.Embed()` |
| Add field | `.addFields({name, value})` | `.add_field(name=, value=)` |
| Get user option | `.getUser('name')` | Parameter in function |
| Fetch member | `guild.members.fetch(id)` | `guild.fetch_member(id)` |
| Get user roles | `member.roles.cache` | `member.roles` |
| Create role | `.roles.create()` | `guild.create_role()` |
| Database query | `await Model.findOne()` | `session.execute(select())` |
| Register event | `client.on('event')` | `@bot.event` |
| Database setup | `sequelize.sync()` | `Base.metadata.create_all()` |

---

## RESOURCES

- Discord.py Docs: https://discordpy.readthedocs.io/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Discord.py Examples: https://github.com/Rapptz/discord.py/tree/master/examples
- Async/Await in Python: https://docs.python.org/3/library/asyncio.html
"""
