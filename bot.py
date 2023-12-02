import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
client = commands.Bot(command_prefix=commands.when_mentioned_or(';'), help_command=None)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
client.run(os.getenv("TOKEN"))
