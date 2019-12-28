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

from core.permissions import has_permission
from discord.ext import commands
import discord
import traceback


class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shutdown', permissions=['admin.shutdown'])
    @has_permission('admin.shutdown')
    async def shutdown(self, ctx):
        if self.bot.isadmin(ctx):
            for VoiceClient in bot.voice_clients:
                await VoiceClient.disconnect()
            await ctx.send("bye bitch")
            await bot.logout()
            quit()
        else:
            await ctx.send("no.")


def setup(bot):
    try:
        bot.add_cog(Shutdown(bot))
    except Exception as e:
        errortb = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f'Error while adding cog "shutdown";\n{errortb}')
