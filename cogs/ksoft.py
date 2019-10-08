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
import datetime
import json
import ksoftapi
import random

print("ksoft.py has been loaded")

with open('config_prod.json', 'r') as cfg:
	config = json.load(cfg)

client = ksoftapi.Client(api_key=config['ksoft'])

def isadmin(ctx):
	"""Checks if the author is an admin"""
	if str(ctx.author.id) not in config['admins']:
		admin = False
	else:
		admin = True
	return admin

imgext = ('.png', '.jpg', '.jpeg', '.gif')

class ksoft(commands.Cog, name="KSoft.SI API"):
	def __init__(self, bot):
		self.bot = bot
		self.bot.ksoft = client

	async def cog_check(self, ctx: commands.Context):
		if ctx.command.name == 'meme' and ctx.guild and ctx.guild.id == 411619823445999637:
			return False
		return True

	@commands.command(description="Gets a random meme from Reddit")
	async def meme(self, ctx, sub: str = None):
		"""PFXmeme [<subreddit>]"""
		if sub == None:
			meme = await self.bot.ksoft.random_meme()
		else:
			meme = await self.bot.ksoft.random_reddit(sub)
		if meme.nsfw:
			channel = ctx.message.channel
			if not channel.is_nsfw():
				await ctx.send("The meme I was given was marked as NSFW but this channel is not. Go into an NSFW channel to see NSFW memes", delete_after=5)
				return
			else:
				pass
		if not meme.title:
			return await ctx.send(f'<a:fireFailed:603214400748257302> The subreddit **{sub}** doesn\'t exist...')
		embed = discord.Embed(title="Did someone order a spicy meme?", colour=ctx.message.author.color, url=meme.source, timestamp=datetime.datetime.utcnow())		
		embed.set_author(name=f"Requested by {ctx.message.author}", icon_url=str(ctx.message.author.avatar_url))
		embed.set_footer(text=f"👍 {meme.upvotes} | 👎 {meme.downvotes} | 💬 {meme.comments} (https://api.ksoft.si)")
		embed.add_field(name="Title", value=meme.title, inline=False)
		embed.add_field(name="Subreddit", value=f"[{meme.subreddit}](https://reddit.com/{meme.subreddit})", inline=False)
		if meme.url:
			if meme.url.endswith(imgext):
				embed.set_image(url=meme.url)
			else:
				embed.add_field(name='Attachment', value=f"[Click Here]({meme.url})")
		else:
			embed.add_field(name='Check it out', value=f'[Click Here]({meme.source})')
		await ctx.send(embed=embed)

	@commands.command(description="Gets a random image from a specified tag", name="image")
	async def randimage(self, ctx, tag: str = None, nsfw: bool = None):
		"""PFXimage [<tag> <nsfw: true/false>]"""
		taglist = await self.bot.ksoft.tags()
		tags = str(taglist).split(', ')
		if tag == 'False':
			nsfw = False
			tag = random.choice(tags)
		elif tag == 'True':
			nsfw = True
			tag = random.choice(tags)
		if tag == None:
			tag = random.choice(tags)
			if tag == None:
				tag = 'dog'
		else:
			if tag not in tags:
				await ctx.send('The tag you gave is invalid. Use the tag command to see a list of tags you can use.')
				return
		channel = ctx.message.channel
		if not channel.is_nsfw():
			nsfw = False
			if tag == 'hentai_gif':
				tag = 'dog'
			if tag == 'neko':
				tag = 'pepe'
		if nsfw == None:
			nsfw = False
		img = await self.bot.ksoft.random_image(tag = tag, nsfw = nsfw)
		if img.nsfw:
			if not channel.is_nsfw():
				msg = await ctx.send("The image I was given was marked as NSFW but this channel is not. Go into an NSFW channel to see NSFW memes", delete_after=5)
				return
		embed = discord.Embed(title="The randomizer machine returned this image!", colour=ctx.message.author.color, url=img.url, timestamp=datetime.datetime.utcnow())
		embed.set_image(url=img.url)
		embed.set_author(name=f"Requested by {ctx.message.author}", icon_url=str(ctx.message.author.avatar_url))
		embed.set_footer(text=f"🏷️ {tag} (https://api.ksoft.si)")
		await ctx.send(embed=embed)

	@commands.command(description="List all available tags")
	async def imagetags(self, ctx):
		"""PFXimagetags"""
		tags = await self.bot.ksoft.tags()
		if ctx.channel.nsfw:
			nsfwtags = ', '.join(tags.nsfw_tags)
			sfwtags = ', '.join(tags.sfw_tags)
			await ctx.send(f'```Non-NSFW Tags:\n{sfwtags}\n\nNSFW Tags:\n{nsfwtags}```')
		else:
			sfwtags = ', '.join(tags.sfw_tags)
			await ctx.send(f'```Tags:\n{sfwtags}```')

	@commands.command(name='baninfo', description='Check the info of a ban on the KSoft.Si API')
	async def baninfo(self, ctx, bannedboi: int):
		'''PFXbaninfo <userid>'''
		ksoftguild: discord.Guild = self.bot.get_guild(458341246453415947)
		check = ksoftguild.get_member(ctx.author.id)
		if not check:
			embed = discord.Embed(title=f"Ban info for {bannedboi}.", colour=ctx.message.author.color, timestamp=datetime.datetime.utcnow())
			embed.add_field(name='Error', value="You must be in the KSoft.Si guild to use this command!\n[Click here to join](https://discord.gg/kEf6qXN 'Click this to join the KSoft.Si API guild')", inline=False)
			return await ctx.send(embed=embed)
		try:
			inf = await self.bot.ksoft.bans_info(bannedboi)
		except ksoftapi.APIError as e:
			embed = discord.Embed(title=f"Ban info for {bannedboi}.", colour=ctx.message.author.color, timestamp=datetime.datetime.utcnow())
			embed.add_field(name='Error', value=e.message, inline=False)
			embed.add_field(name='Code', value=e.code, inline=False)
			return await ctx.send(embed=embed)
		nothingtoseehere = self.bot.get_user(270235302071762945)
		embed = discord.Embed(title=f"Ban info for {bannedboi}.", colour=ctx.message.author.color, timestamp=datetime.datetime.utcnow())
		embed.set_author(name=f"Requested by {ctx.message.author}", icon_url=str(ctx.message.author.avatar_url))
		embed.set_footer(text='Ban info from KSoft.Si API (https://api.ksoft.si/)', icon_url=str(nothingtoseehere.avatar_url))
		embed.add_field(name='User', value=f'{inf.name}#{inf.discriminator}' if inf.name != 'Unknown' else 'Unknown#0000')
		embed.add_field(name='Mod ID', value=inf.moderator_id)
		embed.add_field(name='Active', value=inf.is_ban_active)
		embed.add_field(name='Appeal Possible', value=inf.can_be_appealed)
		embed.add_field(name='Reason', value=inf.reason, inline=False)
		embed.add_field(name='Proof', value=f'[Click Here]({inf.proof})' if inf.proof != 'https://bans.ksoft.si' else 'None Provided')
		embed.add_field(name='Timestamp', value=inf.timestamp.replace('T', ' ').split('.')[0]) # Amazing date formatting code. I call it the date formatter-inator (yes, I am Dr. Doofenshmirtz)
		if inf.appeal_reason and inf.appeal_date:
			embed.add_field(name='Appeal Reason', value=inf.appeal_reason)
			embed.add_field(name='Appeal Date', value=inf.appeal_date.replace('T', ' ').split('.')[0])
		await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(ksoft(bot))