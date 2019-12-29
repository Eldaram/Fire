"""
MIT License
Copyright (c) 2019 GamingGeek

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from discord.ext import commands
from core.fire import Fire
import discord
import aiohttp
import asyncio
import asyncpg
import json


async def get_pre(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return commands.when_mentioned_or('$', 'fire ')(bot, message)
    if not hasattr(bot, 'prefixes'):
        return commands.when_mentioned_or('$', 'fire ')(bot, message)
    prefix = bot.prefixes[message.guild.id] if message.guild.id in bot.prefixes else "$"
    return commands.when_mentioned_or(prefix, 'fire ')(bot, message)


bot = Fire(command_prefix='dev ', status=discord.Status.idle, activity=discord.Game(name="inv.wtf/fire"), case_insensitive=True, owner_id=287698408855044097)
bot.dev = True
bot.authenticated = True


# @bot.check
# async def blacklist_check(ctx):
# 	if ctx.author.id == 287698408855044097:
# 		return True
# 	elif ctx.author.id in ctx.bot.plonked:
# 		return False
# 	else:
# 		return True


# @bot.check
# async def cmdperm_check(ctx):
# 	if isinstance(ctx.channel, discord.DMChannel):
# 		return True
# 	settings = ctx.bot.get_cog('Settings')
# 	if not settings:
# 		return True
# 	if ctx.command.name in settings.disabledcmds.get(ctx.guild.id, []):
# 		if not ctx.author.permissions_in(ctx.channel).manage_messages:
# 			return False
# 		else:
# 			return True
# 	if ctx.guild.id in settings.modonly and ctx.channel.id in settings.modonly[ctx.guild.id]:
# 		if not ctx.author.permissions_in(ctx.channel).manage_messages:
# 			return False
# 		else:
# 			return True
# 	if ctx.guild.id in settings.adminonly and ctx.channel.id in settings.adminonly[ctx.guild.id]:
# 		if not ctx.author.permissions_in(ctx.channel).manage_guild:
# 			return False
# 		else:
# 			return True
# 	return True


async def start_bot():
    try:
        login_data = {"user": "postgres", "password": bot.config['pgpassword'], "database": "fire", "host": "127.0.0.1"}
        bot.db = await asyncpg.create_pool(**login_data)
        await bot.start(bot.config['token'])
    except KeyboardInterrupt:
        await bot.db.close()
        await bot.logout()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
