import discord 
from discord.ext import commands
from config import settings
import asyncio 
import datetime
from db import start_gathering, stop_gathering


intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True

myvoicetime = 0
timetemp = 0

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_voice_state_update(member, before, after):
    global timetemp, myvoicetime
    before_channel_name = before.channel.name if before.channel else 'None'
    after_channel_name = after.channel.name if after.channel else 'None'

    if before.channel is None and after.channel is not None:
        timetemp = datetime.datetime.now()
        guild = client.get_guild(1031866926852477039)
        print(guild)
        print(f"{member.display_name} зашел в {after_channel_name} в {timetemp}")
        # Логика для обработки инфо о пользователях и куда они зашли
    elif before.channel is not None and after.channel is None:
        print(f"{member.display_name} вышел из {before_channel_name} в {datetime.datetime.now()}")
        myvoicetime = datetime.datetime.now() - timetemp
        print(f"{member.display_name} был в воисе {myvoicetime}")
        # Логика для обработки инфо о пользователях и куда они вышли

# @client.event
# async def on_message(message, member: discord.Member = None):
#     print(message.author, message.content, ) 

@commands.has_guild_permissions(administrator=True)
@client.command()
async def start(ctx):
    await ctx.message.delete()
    # Логика для включения сбора статистики
    await start_gathering(ctx.message.guild.name, ctx.message.guild.id, ctx.message.guild.member_count, True)
    
    # await ctx.send("Бот начинает собирать статистику")

@commands.has_guild_permissions(administrator=True)
@client.command()
async def stop(ctx):
    await ctx.message.delete()
    await stop_gathering(ctx.message.guild.id)
    
    # await ctx.send("Бот не собирает статистику")

async def main():
    async with client:
        await client.start(settings.bot_token)

if __name__ == '__main__':
    asyncio.run(main())