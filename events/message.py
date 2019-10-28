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

from core.context import Context
from discord.ext import commands
import functools
import asyncio
import discord

class Message(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			await self.bot.loop.run_in_executor(None, func=functools.partial(self.bot.datadog.increment, 'messages.bot'))
			return
		else:
			await self.bot.loop.run_in_executor(None, func=functools.partial(self.bot.datadog.increment, 'messages.user'))
		if message.system_content == "":
			return
		ctx = await self.bot.get_context(message, cls=Context)
		if not ctx.valid:
			return
        await self.bot.invoke(ctx)

def setup(bot):
	try:
		bot.add_cog(Message(bot))
	except Exception as e:
		errortb = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
		print(f'Error while adding cog "Message";\n{errortb}')