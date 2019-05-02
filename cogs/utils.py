import discord
from discord.ext import commands
import datetime
import json
import time
import os
import typing
import re
import aiosqlite3
from jishaku.paginators import PaginatorInterface, WrappedPaginator
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

launchtime = datetime.datetime.utcnow()

print('utils.py has been loaded')

with open('config.json', 'r') as cfg:
	config = json.load(cfg)
	error_string = config['response_string']['error']
	success_string = config['response_string']['success']

def isadmin(ctx):
	'''Checks if the author is an admin'''
	if str(ctx.author.id) not in config['admins']:
		admin = False
	else:
		admin = True
	return admin

snipes = {}
disabled = [264445053596991498, 110373943822540800, 336642139381301249, 458341246453415947]

def snipe_embed(context_channel, message, user):
	if message.author not in message.guild.members or message.author.color == discord.Colour.default():
		embed = discord.Embed(description = message.content, timestamp = message.created_at)
	else:
		embed = discord.Embed(description = message.content, color = message.author.color, timestamp = message.created_at)
	embed.set_author(name = str(message.author), icon_url = message.author.avatar_url)
	if message.attachments:
		embed.add_field(name = 'Attachment(s)', value = '\n'.join([attachment.filename for attachment in message.attachments]) + '\n\n__Attachment URLs are invalidated once the message is deleted.__')
	if message.channel != context_channel:
		embed.set_footer(text = 'Sniped by: ' + str(user) + ' | in channel: #' + message.channel.name)
	else:
		embed.set_footer(text = 'Sniped by: ' + str(user))
	return embed

def quote_embed(context_channel, message, user):
	if not message.content and message.embeds and message.author.bot:
		embed = message.embeds[0]
	else:
		if message.author not in message.guild.members or message.author.color == discord.Colour.default():
			embed = discord.Embed(timestamp = message.created_at)
			embed.add_field(name='Message', value=message.content, inline=False)
			embed.add_field(name='Jump URL', value=f'[Click Here]({message.jump_url})', inline=False)
		else:
			embed = discord.Embed(color = message.author.color, timestamp = message.created_at)
			embed.add_field(name='Message', value=message.content, inline=False)
			embed.add_field(name='Jump URL', value=f'[Click Here]({message.jump_url})', inline=False)
		if message.attachments:
			if message.channel.is_nsfw() and not context_channel.is_nsfw():
				embed.add_field(name = 'Attachments', value = ':underage: Quoted message is from an NSFW channel.')
			elif len(message.attachments) == 1 and message.attachments[0].url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv', '.webp', '.bmp')):
				embed.set_image(url = message.attachments[0].url)
			else:
				for attachment in message.attachments:
					embed.add_field(name = 'Attachment', value = '[' + attachment.filename + '](' + attachment.url + ')', inline = False)
		embed.set_author(name = str(message.author), icon_url = message.author.avatar_url, url = 'https://discordapp.com/channels/' + str(message.guild.id) + '/' + str(message.channel.id) + '/' + str(message.id))
		if message.channel != context_channel:
			embed.set_footer(text = 'Quoted by: ' + str(user) + ' | #' + message.channel.name)
		else:
			embed.set_footer(text = 'Quoted by: ' + str(user))
	return embed

def getGame(activity):
	game = str(activity)
	game = game.lower()
	check = game
	if 'minecraft' in game:
		game = '<:Minecraft:516401572755013639> Minecraft'
	if 'hyperium' in game:
		game = '<:Hyperium:516401570741485573> Hyperium'
	if 'badlion client' in game:
		game = '<:BLC:516401568288079892> Badlion Client'
	if 'labymod' in game:
		game = '<:LabyMod:531495743295586305> LabyMod'
	if 'fortnite' in game:
		game = '<:Fortnite:516401567990153217> Fortnite'
	csgo = ['csgo', 'counter-strike']
	for string in csgo: 
		if string in game:
			game = '<:CSGO:516401568019513370> CS:GO'
	pubg = ['pubg', 'playerunknown\'s battlegrounds']
	for string in pubg:
		if string in game:
			game =  '<:PUBG:516401568434618388> PUBG'
	gta = ['gta v', 'grand theft auto v']
	for string in gta:
		if string in game:
			game = '<:GTAV:516401570556936232> GTA V'
	if 'roblox' in game:
		game = '<:Roblox:516403059673530368> Roblox'
	if 'payday 2' in game:
		game = '<:PayDayTwo:516401572847157248> Payday 2'
	if 'overwatch' in game:
		game = '<:Overwatch:516402281806037002> Overwatch'
	if 'portal' in game:
		game = '<:Portal:516401568610779146> Portal'
	if 'geometry dash' in game:
		game = '<:GeometryDash:516403764635238401> Geometry Dash'
	if 'spotify' in game:
		game = '<:Spotify:516401568812105737> Spotify'
	if 'netflix' in game:
		game = '<:Netflix:472000254053580800> Netflix'
	if 'google chrome' in game:
		game = '<:chrome:556997945677840385> Chrome'
	if 'firefox' in game:
		game = '<:FIREFOX:516402280916975637> Firefox'
	if 'internet explorer' in game:
		game = '<:IEXPLORE:516401569005174795> Internet Explorer'
	if 'safari' in game:
		game = '<:SAFARI:516401571433807882> Safari'
	if 'visual studio' in game:
		game = '<:VSCODE:516401572943495169> Visual Studio'
	if 'visual studio code' in game:
		game = '<:VSCODE:516401572943495169> Visual Studio Code'
	if 'jetbrains ide' in game:
		game = '<:jetbrains:556999976496922634> JetBrains IDE'
	if 'sublime text' in game:
		game = '<:SUBLIME:516401568531218454> Sublime Text'
	if 'atom editor' in game:
		game = '<:ATOMEDIT:516401571232219136> Atom'
	if 'vegas pro' in game:
		game = '<:VEGAS:516401568598458378> Vegas Pro'
	if 'after effects' in game:
		game = '<:AE:516401568124370954> After Effects'
	if 'adobe illustrator' in game:
		game = '<:AI:516401567411208227> Illustrator'
	if 'adobe animate' in game:
		game = '<:AN:516401568648790026> Animate'
	if 'adobe audition' in game:
		game = '<:AU:516401568678150144> Audition'
	if 'photoshop' in game:
		game = '<:PS:516401568149536790> Photoshop'
	if 'adobe xd' in game:
		game = '<:XD:516401572708876313> xD'
	if 'premiere pro' in game:
		game = '<:PR:516401568841596968> Premiere Pro'
	if 'blender' in game:
		game = '<:BLEND:516401568321634314> Blender'
	if 'cinema 4d' in game:
		game = '<:C4D:516401570741616659> Cinema 4D'
	if check == game:
		game = str(activity)
	return game

class utils(commands.Cog, name='Utility Commands'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='bl.add', description='Add someone to the blacklist', hidden=True)
	async def blacklist_add(self, ctx, user: discord.User = None, reason: str = 'bad boi', permanent: bool = False):
		'''Add a user to the blacklist or Update a user on the blacklist. (Note: bc im lazy, values will reset to default if not provided)'''
		if isadmin(ctx) == False:
			return
		if user == None:
			await ctx.send('You need to provide a user to add to the blacklist!')
		else:
			await self.bot.db.execute(f'SELECT * FROM blacklist WHERE uid = {user.id};')
			blraw = await self.bot.db.fetchone()
			if blraw == None:
				if permanent == True:
					permanent = 1
				else:
					permanent = 0
				await self.bot.db.execute(f'INSERT INTO blacklist (\"user\", \"uid\", \"reason\", \"perm\") VALUES (\"{user}\", {user.id}, \"{reason}\", {permanent});')
				await self.bot.conn.commit()
				await ctx.send(f'{user.mention} was successfully blacklisted!')
			else:
				blid = blraw[0]
				if permanent == True:
					permanent = 1
				else:
					permanent = 0
				await self.bot.db.execute(f'UPDATE blacklist SET user = \"{user}\", uid = {user.id}, reason = \"{reason}\", perm = {permanent} WHERE id = {blid};')
				await self.bot.conn.commit()
				await ctx.send(f'Blacklist entry updated for {user.mention}.')

	@commands.command(name='bl.remove', description='Remove someone from the blacklist', hidden=True)
	async def blacklist_remove(self, ctx, user: discord.User = None):
		'''Remove a user from the blacklist'''
		if isadmin(ctx) == False:
			return
		if user == None:
			await ctx.send('You need to provide a user to remove from the blacklist!')
		else:
			await self.bot.db.execute(f'SELECT * FROM blacklist WHERE uid = {user.id};')
			blraw = await self.bot.db.fetchone()
			if blraw == None:
				await ctx.send(f'{user.mention} is not blacklisted.')
				return
			else:
				await self.bot.db.execute(f'DELETE FROM blacklist WHERE uid = {user.id};')
				await self.bot.conn.commit()
				await ctx.send(f'{user.mention} is now unblacklisted!')


	@commands.command(description='Bulk delete messages')
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, amount: int=None):
		'''Purge an amount of messages in a channel
		-------------------------
		Ex:
		$purge 50'''
		if amount is None:
			return await ctx.send(f'Hey, please do `purge [amount]`!')
		if amount>500 or amount<0:
			return await ctx.send('Invalid amount. Maximum is 500')
		await ctx.message.delete()
		await ctx.message.channel.purge(limit=amount)
		await ctx.send(f'Sucesfully deleted **{int(amount)}** messages!', delete_after=5)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		try:
			del snipes[guild.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		try:
			del snipes[channel.guild.id][channel.id]
		except KeyError:
			pass

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.guild and not message.author.bot:
			try:
				snipes[message.guild.id][message.channel.id] = message
			except KeyError:
				snipes[message.guild.id] = {message.channel.id: message}

	@commands.command(description='Get the last deleted message')
	async def snipe(self, ctx, channel: typing.Union[discord.TextChannel, int] = None):
		'''Get the last deleted message'''
		if type(channel) == int:
			channel = self.bot.get_channel(channel)
		if not channel:
			channel = ctx.channel

		if not ctx.author.permissions_in(channel).read_messages:
			return

		try:
			sniped_message = snipes[ctx.guild.id][channel.id]
		except KeyError:
			return await ctx.send(content = ':x: **No available messages.**')
		else:
			await ctx.send(embed = snipe_embed(ctx.channel, sniped_message, ctx.author))

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == '💬' and not self.bot.get_guild(payload.guild_id).get_member(payload.user_id).bot:
			guild = self.bot.get_guild(payload.guild_id)
			channel = guild.get_channel(payload.channel_id)
			user = guild.get_member(payload.user_id)

			if user.permissions_in(channel).send_messages:
				try:
					message = await channel.fetch_message(payload.message_id)
				except discord.NotFound:
					return
				except discord.Forbidden:
					return
				else:
					if not message.content and message.embeds and message.author.bot:
						await channel.send(content = 'Raw embed from `' + str(message.author).strip('`') + '` in ' + message.channel.mention, embed = quote_embed(channel, message, user))
					else:
						await channel.send(embed = quote_embed(channel, message, user))

	@commands.Cog.listener()
	async def on_message(self, message):
		if 'fetchmsg' in message.content:
			return
		if 'quote' in message.content:
			return
		if message.guild != None:
			if message.guild.id in disabled:
				return
			perms = message.guild.me.permissions_in(message.channel)
			if not perms.send_messages or not perms.embed_links or message.author.bot:
				return

			for i in message.content.split():
				word = i.lower().strip('<>')
				if word.startswith('https://canary.discordapp.com/channels/'):
					word = word.strip('https://canary.discordapp.com/channels/')
				elif word.startswith('https://ptb.discordapp.com/channels/'):
					word = word.strip('https://ptb.discordapp.com/channels/')
				elif word.startswith('https://discordapp.com/channels/'):
					word = word.strip('https://discordapp.com/channels/')
				else:
					continue

				list_ids = word.split('/')
				if len(list_ids) == 3:
					del list_ids[0]

					try:
						channel = self.bot.get_channel(int(list_ids[0]))
					except:
						continue

					if channel and isinstance(channel, discord.TextChannel):
						try:
							msg_id = int(list_ids[1])
						except:
							continue

						try:
							msg_found = await channel.fetch_message(msg_id)
						except:
							continue
						else:
							if not msg_found.content and msg_found.embeds and msg_found.author.bot:
								await message.channel.send(content = 'Raw embed from `' + str(msg_found.author).strip('`') + '` in ' + msg_found.channel.mention, embed = quote_embed(message.channel, msg_found, message.author))
							else:
								await message.channel.send(embed = quote_embed(message.channel, msg_found, message.author))

	@commands.command(description='Quote a message from an id or url')
	async def quote(self, ctx, msg: typing.Union[str, int] = None):
		'''Quote a message from an id or url'''
		if not msg:
			return await ctx.send(content = error_string + ' Please specify a message ID/URL to quote.')
		try:
			msg_id = int(msg)
		except Exception:
			msg_id = str(msg)
		if type(msg_id) == int:
			message = None
			try:
				message = await ctx.channel.fetch_message(msg_id)
			except:
				for channel in ctx.guild.text_channels:
					perms = ctx.guild.me.permissions_in(channel)
					if channel == ctx.channel or not perms.read_messages or not perms.read_message_history:
						continue

					try:
						message = await channel.fetch_message(msg_id)
					except:
						continue
					else:
						break

			if message:
				if not message.content and message.embeds and message.author.bot:
					await ctx.send(content = 'Raw embed from `' + str(message.author).strip('`') + '` in ' + message.channel.mention, embed = quote_embed(ctx.channel, message, ctx.author))
				else:
					await ctx.send(embed = quote_embed(ctx.channel, message, ctx.author))
			else:
				await ctx.send(content = error_string + ' I couldn\'t find that message...')
		else:
			perms =  ctx.guild.me.permissions_in( ctx.channel)
			if not perms.send_messages or not perms.embed_links or  ctx.author.bot:
				return

			for i in msg_id.split():
				word = i.lower().strip('<>')
				if word.startswith('https://canary.discordapp.com/channels/'):
					word = word.strip('https://canary.discordapp.com/channels/')
				elif word.startswith('https://ptb.discordapp.com/channels/'):
					word = word.strip('https://ptb.discordapp.com/channels/')
				elif word.startswith('https://discordapp.com/channels/'):
					word = word.strip('https://discordapp.com/channels/')
				else:
					continue

				list_ids = word.split('/')
				if len(list_ids) == 3:
					del list_ids[0]

					try:
						channel = self.bot.get_channel(int(list_ids[0]))
					except:
						continue

					if channel and isinstance(channel, discord.TextChannel):
						try:
							msg_id = int(list_ids[1])
						except:
							continue

						try:
							msg_found = await channel.fetch_message(msg_id)
						except:
							continue
						else:
							if not msg_found.content and msg_found.embeds and msg_found.author.bot:
								await ctx.send(content = 'Raw embed from `' + str(msg_found.author).strip('`') + '` in ' + msg_found.channel.mention, embed = quote_embed(ctx.channel, msg_found, ctx.author))
							else:
								await ctx.send(embed = quote_embed(ctx.channel, msg_found, ctx.author))

	@commands.command(description='Got a HTTP Error Code? My cat knows what it means.', name='http.cat')
	async def httpcat(self, ctx, error: int = 200):
		'''Got a HTTP Error Code? My cat knows what it means.'''
		embed = discord.Embed(color=ctx.author.color)
		embed.set_image(url=f'https://http.cat/{error}')
		await ctx.send(embed=embed)

	@commands.command(description='Fetch a channel and get some beautiful json')
	async def fetchchannel(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel] = None):
		'''Return a channel as beautiful json'''
		if channel is None:
			channel = ctx.channel

		route = discord.http.Route("GET", f"/channels/{channel.id}")
		try:
			raw = await ctx.bot.http.request(route)
		except discord.HTTPException:
			raise commands.UserInputError('Couldn\'t find that channel.')
			return

		try:
			await ctx.send(f"```json\n{json.dumps(raw, indent=2)}```")
		except discord.HTTPException as e:
			e = str(e)
			if 'Must be 2000 or fewer in length' in e:
				paginator = WrappedPaginator(prefix='```json', suffix='```', max_size=1895)
				paginator.add_line(json.dumps(raw, indent=2))
				interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
				await interface.send_to(ctx)

	@commands.command(description='Fetch a channel from it\'s id or link')
	async def fetchmsg(self, ctx, msg: typing.Union[str, int] = None):
		'''Returns a message as beautiful json'''
		try:
			msg = int(msg)
		except Exception:
			pass
		if type(msg) == int:
			message = None
			try:
				message = await ctx.channel.fetch_message(msg)
			except:
				for channel in ctx.guild.text_channels:
					perms = ctx.guild.me.permissions_in(channel)
					if channel == ctx.channel or not perms.read_messages or not perms.read_message_history:
						continue

					try:
						message = await channel.fetch_message(msg)
					except:
						continue
					else:
						break
			if message:
				raw = await ctx.bot.http.get_message(message.channel.id, message.id)
				try:
					await ctx.send(f"```json\n{json.dumps(raw, indent=2)}```")
				except discord.HTTPException as e:
					e = str(e)
					if 'Must be 2000 or fewer in length' in e:
						paginator = WrappedPaginator(prefix='```json', suffix='```', max_size=1895)
						paginator.add_line(json.dumps(raw, indent=2))
						interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
						await interface.send_to(ctx)
			else:
				raise commands.UserInputError('Message could not be found. Make sure you have the right id')
		elif type(msg) == str:
			for i in msg.split():
				word = i.lower().strip('<>')
				if word.startswith('https://canary.discordapp.com/channels/'):
					word = word.strip('https://canary.discordapp.com/channels/')
				elif word.startswith('https://ptb.discordapp.com/channels/'):
					word = word.strip('https://ptb.discordapp.com/channels/')
				elif word.startswith('https://discordapp.com/channels/'):
					word = word.strip('https://discordapp.com/channels/')
				else:
					continue
			list_ids = word.split('/')
			try:
				test = list_ids[1]
			except IndexError:
				raise commands.UserInputError(f'Unable to retrieve a message from {msg}')
				return
			if len(list_ids) == 3:
				del list_ids[0]
			chanid = list_ids[0]
			msgid = list_ids[1]
			raw = await ctx.bot.http.get_message(chanid, msgid)
			try:
				await ctx.send(f"```json\n{json.dumps(raw, indent=2)}```")
			except discord.HTTPException as e:
				e = str(e)
				if 'Must be 2000 or fewer in length' in e:
					paginator = WrappedPaginator(prefix='```json', suffix='```', max_size=1895)
					paginator.add_line(json.dumps(raw, indent=2))
					interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
					await interface.send_to(ctx)
		else:
			raise commands.UserInputError('Message argument was neither an id or url')


	@commands.command(description='Find a user from their id')
	async def fetchuser(self, ctx, user: int = None):
		'''Find a user from their id'''
		if user == None:
			user = ctx.message.author.id
		try:
			fetched = self.bot.get_user(user)
		except Exception as e:
			raise commands.UserInputError('Oops, couldn\'t find that user. I need to be in a server with them')
		if fetched == None:
			if isadmin(ctx):
				try:
					fetched = await self.bot.fetch_user(user)
				except discord.NotFound:
					raise commands.UserInputError('Hmm.... I can\'t seem to find that user')
					return
				except discord.HTTPException:
					raise commands.UserInputError('Something went wrong when trying to find that user...')
					return
			else:
				raise commands.UserInputError('Hmm.... I can\'t seem to find that user')
				return
		userInfo = {
			'name': fetched.name,
			'discrim': fetched.discriminator,
			'id': fetched.id,
			'bot': fetched.bot,
			'avatar': fetched.avatar
		}
		user = json.dumps(userInfo, indent=2)
		embed = discord.Embed(title=f'Found user {fetched}', description=f'```json\n{user}```')
		await ctx.send(embed=embed)
	
	@commands.command(description='Get user info in an image. (proof of concept)')
	async def imgtest(self, ctx, user: discord.Member = None):
		'''this is just a test for now...'''
		if user == None:
			user = ctx.author
		await ctx.send(f'Retrieving {user}\'s info')
		img = Image.open('cogs/infoimgimg.png')
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype('cogs/Modern_Sans_Light.otf', 100)
		fontbig = ImageFont.truetype('cogs/Fitamint Script.ttf', 400)
		draw.text((200, 0), 'Information:', (255, 255, 255), font=fontbig)
		draw.text((50, 500), f'Username: {user.name}', (255, 255, 255), font=font)
		draw.text((50, 700), f'ID: {user.id}', (255, 255, 255), font=font)
		draw.text((50, 900), f'User Status: {user.status}', (255, 255, 255), font=font)
		draw.text((50, 1100), f'Account created: {user.created_at}', (255, 255, 255), font=font)
		draw.text((50, 1300), f'Nickname: {user.display_name}', (255, 255, 255), font=font)
		draw.text((50, 1500), f'{user.name}\'s Top Role: {user.top_role}', (255, 255, 255), font=font)
		draw.text((50, 1700), f'User Joined: {user.joined_at}', (255, 255, 255), font=font)
		img.save(f'cogs/{user.id}.png')
		image = discord.File(f'cogs/{user.id}.png', filename=f'{user.id}.png', spoiler=False)
		await ctx.send(file=image)
		uid = user.id
		if os.path.exists(f"cogs/{uid}.png"):
			os.remove(f'cogs/{uid}.png')
		else:
			await ctx.send('error deleting file.')
		
def setup(bot):
	bot.add_cog(utils(bot))