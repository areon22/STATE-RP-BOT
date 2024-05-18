import discord
from discord.ext import commands
import asyncio
import os
import schedule


bot = discord.Bot()
cogsfile = [f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")]

for cog in cogsfile:
    try:
        bot.load_extension(cog)
    except Exception as err:
            print(err)
   
@bot.event
async def on_ready():
        print(f'{bot.user.name} запущен')
        
@bot.event
async def on_connect():
     print(f'{bot.user.name} подключился')

bot.run('MTE5ODU3MjczMTQ4NzIzNjE5Ng.Gq70W2.h0x25ShEt8PEa_Re_tzSNl-r7zakCoEytELVQM')

        
        




