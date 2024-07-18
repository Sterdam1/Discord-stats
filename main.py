import discord 
from discord.ext import commands
from config import settings
import asyncio 

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_voice_state_update(member, before, after):
    before_channel_name = before.channel.name if before.channel else 'None'
    after_channel_name = after.channel.name if after.channel else 'None'

    if before.channel is None and after.channel is not None:
        guild = client.get_guild(1031866926852477039)
        print(guild)
        print(f"{member.display_name} зашел в {after_channel_name}")
        # Логика для обработки инфо о пользователях и куда они зашли
    elif before.channel is not None and after.channel is None:
        print(f"{member.display_name} вышел из {before_channel_name}")
        # Логика для обработки инфо о пользователях и куда они вышли

@client.event
async def on_message(message):
    print(message.author, message.content) 

@client.command()
async def start(ctx):
    await ctx.message.delete()
    # Логика для включения сбора статистики
    await ctx.send("Бот начинает собирать статистику")

@client.command()
async def stop(ctx):
    await ctx.message.delete()
    # Логика для выключения сбора статистики
    await ctx.send("Бот не собирает статистику")

async def main():
    async with client:
        await client.start(settings.bot_token)

if __name__ == '__main__':
    asyncio.run(main())