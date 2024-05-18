import time
import discord
from discord.ext import commands
import asyncio

class Servese(commands.Cog):   
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        print('Модуль Servese запушен')
    
    @discord.command(description='Отчистка чата команда вводится как /clear num, где num это ваше число.')
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.respond(f"> Удалено **{amount}** сообщений.")
        time.sleep(3)
        await ctx.channel.purge(limit=1)
        
def setup(bot):
    bot.add_cog(Servese(bot))
