import discord 
from discord.ext import commands
from config import settings
import asyncio 

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def start(ctx):
    print(ctx.message)
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