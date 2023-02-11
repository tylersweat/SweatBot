#!/usr/bin/env python3

import discord
from discord.ext import commands
import json
import requests
from decouple import config
import osrs_stats
from io import BytesIO

# Get bot token from .env
DISCORD_TOKEN = config('DISCORD_TOKEN')

# Define various globals.
GENERAL_CHANNEL = 817472812671434786    # Channel ID for general channel where we want people to add roles.

CHANNELS = {
    'general': 817472812671434786,
    'invite': 817476581395529749,
    'dev': 818927657370124310,
    'osrs': 817472902877413376,
    'drops': 818905712922460220,
    'rock-climbing': 817472931437084732,
    'spikeball': 817472999795458048,
    'road-trip': 817477201170530425,
    'hiking': 817476482170880061,
    'misc': 817487027414630452,
    'game-night': 818942629911724062,
    'among-us': 817473279216320513,
    'chess': 817473890048671786,
    'memes': 817486842273464440,
    'chat': 819001618707251200
}

SELF_SERVE_ROLES = ['osrs', 'chess', 'spikeball', 'rock-climber', 'road trippin\'', 'hiker', 'memer', 'board games', 'movies', 'i\'m sus']

# Define the bot client.
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}!')

@client.command()
async def test(ctx):
    await ctx.message.reply('Yup, I\'m here.')

@client.command()
async def osrs(ctx):
    if ctx.message.channel.id == CHANNELS['general']:
        # Get member issuing command.
        member = ctx.message.author
        role = discord.utils.get(member.guild.roles, name='osrs')
        await member.add_roles(role)
        await ctx.message.delete()
    else:
        pass

@client.command()
async def stats(ctx, *rsn: str):
    if ctx.message.channel.name != 'osrs':
        await ctx.message.reply('Try that command in the #osrs channel!')
    else:
        _rsn = ' '.join(rsn)
        img = BytesIO()
        osrs_stats.create_stats(_rsn, img)
        await ctx.channel.send(content=f'Stats for {_rsn}',file=discord.File(img,f'{_rsn}_stats.png'))
        #await ctx.message.delete(delay=60)  # Delete original message after 60s to clear up channel.


@stats.error
async def stats_error(ctx, error):
    print(error)
    await ctx.message.delete()

@client.command()
async def chess(ctx, min: int=10, inc: int=3):
    if ctx.message.channel.name != 'chess':
        await ctx.message.reply('Try that command in the #chess channel!')
    else:
        if min <= 0:
            # Set for correspondence game.
            time = None
            inc = None
        else:
            time = min * 60
        game = {'clock.limit': time, 'clock.increment': inc, 'variant': 'standard'}
        r = requests.post('https://lichess.org/api/challenge/open', data=game)
        url = r.json()['challenge']['url']
        await ctx.message.channel.send('New challenge issued: {0}'.format(url))

@chess.error
async def chess_error(ctx, error):
    print(error)

@client.command()
async def join(ctx, roles: commands.Greedy[discord.Role]):
    member = ctx.message.author
    for role in roles:
        if role.name in SELF_SERVE_ROLES:
            await member.add_roles(role)
    await ctx.message.delete()

@client.command()
async def leave(ctx, roles: commands.Greedy[discord.Role]):
    member = ctx.message.author
    for role in roles:
        if role.name in SELF_SERVE_ROLES:
            await member.remove_roles(role)
    await ctx.message.delete()

@join.error
async def join_error(ctx, error):
    print(error)

@leave.error
async def leave_error(ctx, error):
    pass



# Log in as the bot client.
client.run(DISCORD_TOKEN)
