from discord.ext import commands
from discord.utils import get
import discord
import json

import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents  # Set up basic permissions
)


bot.author_id = "191868731838693376"  # Change to your discord id


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

# WARMUP PART


@bot.command()
async def pong(ctx):
    await ctx.send('pong')


@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))

# Respond with author's name


@bot.command()
async def name(ctx):
    await ctx.send(ctx.message.author.name)


# ADMIN PART

@bot.command()
async def admin(ctx, member: discord.Member = None):
    # Prevent command calls without arg
    if not member:
        await ctx.send('Please mention a user')
    else:
        # Check if role exists, if not we create it
        if not get(ctx.guild.roles, name="Admin"):
            print("Creating role: Admin")
            perms = discord.Permissions(8)
            await ctx.guild.create_role(name="Admin", permissions=perms)
        # We give role to user
        print("Giving role to user: " + member.name)
        role = get(ctx.guild.roles, name="Admin")
        await member.add_roles(role)


@bot.command()
async def ban(ctx, member: discord.Member = None):
    print("Banishing: " + member.name)
    await member.ban(reason="Oust")


@bot.command()
async def count(ctx):
    class Stats:
        online = 0
        offline = 0
        idle = 0
        DND = 0

    status = Stats()
    for guild in bot.guilds:
        print("Members in server: " + guild.name)
        for member in guild.members:
            print("Count, member.name: " + member.name)
            print("Count, member.status: " + member.status.name)
            if member.status.name == "online":
                status.online += 1
            elif member.status.name == "offline":
                status.offline += 1
            elif member.status.name == "idle":
                status.idle += 1
            else:
                status.DND += 1
    message = "Active members: " + str(status.online) + "\n"
    message += "Offline members: " + str(status.offline) + "\n"
    message += "Idle members: " + str(status.idle) + "\n"
    message += "DND members: " + str(status.DND) + "\n"
    print("Count: " + message)
    await ctx.send(message)


# React to a message sent in a channel
@bot.event
async def on_message(message):
    # Avoid answering to self-sent messages
    if message.author == bot.user:
        return

    # Respond to "Salut tout le monde " and ping the sender
    if message.content.startswith('Salut tout le monde'):
        await message.channel.send("Salut tout seul " + '{}'.format(message.author.mention))
    await bot.process_commands(message)

# Secret token handling
f = open("config/config.json")

data = json.load(f)
f.close()

if "token" in data:
    bot.run(data["token"])
else:
    print("Token cannot be read")
    exit
