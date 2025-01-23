import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Variables to store channel settings
welcome_channel = None
leave_channel = None
log_channel = None
premium_users = {}
premium_role = None
command_roles = {}

# Bot Ready Event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Setup command
@bot.command()
async def setup(ctx, option: str, channel: discord.TextChannel):
    global welcome_channel, leave_channel, log_channel
    if option == "welcome":
        welcome_channel = channel.id
        await ctx.send(f"Welcome channel set to {channel.mention}")
    elif option == "leave":
        leave_channel = channel.id
        await ctx.send(f"Leave channel set to {channel.mention}")
    elif option == "log":
        log_channel = channel.id
        await ctx.send(f"Log channel set to {channel.mention}")
    else:
        await ctx.send("Invalid option. Use 'welcome', 'leave', or 'log'.")

# Ban command
@bot.command()
async def ban(ctx, member: discord.Member, duration: str):
    await ctx.send(f"{member.mention} has been banned for {duration}")

# Kick command
@bot.command()
async def kick(ctx, member: discord.Member):
    await ctx.send(f"{member.mention} has been kicked")

# Timeout command
@bot.command()
async def timeout(ctx, member: discord.Member, duration: str):
    await ctx.send(f"{member.mention} has been timed out for {duration}")

# User Lookup command
@bot.command()
async def user_look_up(ctx, user: discord.User):
    embed = discord.Embed(title=f"User Info: {user.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="User ID", value=user.id, inline=True)
    embed.add_field(name="Created At", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)

# Generate premium access key
@bot.command()
async def generate(ctx):
    key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(6, 18)))
    await ctx.author.send(f"Your access key: `{key}`")

# Premium commands
@bot.command()
async def premium(ctx, user: discord.Member):
    premium_users[user.id] = True
    await ctx.send(f"{user.mention} is now a premium user!")

@bot.command()
async def premium_delete(ctx, user: discord.Member):
    premium_users.pop(user.id, None)
    await ctx.send(f"Premium removed from {user.mention}")

@bot.command()
async def premium_role(ctx, role: discord.Role):
    global premium_role
    premium_role = role.id
    await ctx.send(f"Premium role set to {role.name}")

@bot.command()
async def premium_list(ctx):
    if premium_users:
        user_list = "\n".join([f"<@{user_id}>" for user_id in premium_users.keys()])
        await ctx.send(f"Premium users:\n{user_list}")
    else:
        await ctx.send("No premium users.")

# Role-linking for commands
@bot.command()
async def set(ctx, role: discord.Role, command: str):
    command_roles[command] = role.id
    await ctx.send(f"Command `{command}` now requires `{role.name}` role.")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
