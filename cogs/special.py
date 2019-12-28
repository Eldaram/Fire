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

import discord
from discord.ext import commands
from cogs.moderation import StaffCheckNoMessage
from jishaku.models import copy_context_with
import datetime
import asyncio
import random

print("special.py has been loaded")

class special(commands.Cog, name="Special Commands"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='trickortreat')
	@commands.guild_only()
	@commands.cooldown(1, 120, commands.BucketType.user)
	async def trickortreat(self, ctx):
		choices = ['mute-15m', 'meme', 'mute-30m', 'warn', 'meme', 'meme', 'meme', 'meme', 'gassist-joke', 'gassist-joke', 'gassist-joke']
		chosen = random.choice(choices)
		if chosen == 'mute-15m':
			await ctx.send(f'I\'m searching through my tricks and treats and for you I have.... a 15 minute mute! Mwahahahahaa.')
			if not ctx.guild.me.guild_permissions.manage_roles:
				await asyncio.sleep(1)
				return await ctx.send('Darn it! I don\'t seem to have permission to manage roles. You got lucky this time...')
			else:
				isStaff = await StaffCheckNoMessage().convert(ctx, str(ctx.author.id))
				if not isStaff:
					await asyncio.sleep(1)
					return await ctx.send('It seems you are immune to my mutes. Curse you Manage Messages permission!!!')
				else:
					alt_ctx = await copy_context_with(ctx, author=ctx.guild.me, content=ctx.prefix + f'mute {ctx.author.id} 15m Recieved a trick instead of a treat...')
					return await alt_ctx.command.reinvoke(alt_ctx)
		elif chosen == 'mute-30m':
			await ctx.send(f'I\'m searching through my tricks and treats and for you I have.... a 30 minute mute! Mwahahahahaa.')
			if not ctx.guild.me.guild_permissions.manage_roles:
				await asyncio.sleep(1)
				return await ctx.send('Darn it! I don\'t seem to have permission to manage roles. You got lucky this time...')
			else:
				isStaff = await StaffCheckNoMessage().convert(ctx, str(ctx.author.id))
				if not isStaff:
					await asyncio.sleep(1)
					return await ctx.send('It seems you are immune to my mutes. Curse you Manage Messages permission!!!')
				else:
					alt_ctx = await copy_context_with(ctx, author=ctx.guild.me, content=ctx.prefix + f'mute {ctx.author.id} 30m Recieved a trick instead of a treat...')
					return await alt_ctx.command.reinvoke(alt_ctx)
		elif chosen == 'warn':
			await ctx.send(f'I\'m searching through my tricks and treats and for you I have.... a warning! Mwahahahahaa.')
			alt_ctx = await copy_context_with(ctx, author=ctx.guild.me, content=ctx.prefix + f'warn {ctx.author.id} Wasn\'t so lucky and recieved a trick instead of a treat...')
			return await alt_ctx.command.reinvoke(alt_ctx)
		elif chosen == 'meme':
			await ctx.send(f'I\'m searching through my tricks and treats and for you I have.... a random meme! You were lucky this time.')
			alt_ctx = await copy_context_with(ctx, content=ctx.prefix + 'meme')
			return await alt_ctx.command.reinvoke(alt_ctx)
		elif chosen == 'gassist-joke':
			await ctx.send(f'I\'m searching through my tricks and treats and for you I have.... a joke from the Google Assistant! You were lucky this time (unless you hate jokes).')
			alt_ctx = await copy_context_with(ctx, content=ctx.prefix + 'gassist tell me a joke')
			return await alt_ctx.command.reinvoke(alt_ctx)


def setup(bot):
	bot.add_cog(special(bot))