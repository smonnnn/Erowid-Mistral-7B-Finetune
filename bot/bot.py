# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import gen

description = 'DMT BOT'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)
model, tokenizer = gen.setup()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(description='Prompt the model.')
async def prompt(ctx, prompt: str, length: int):
    """Chooses between multiple choices."""
    response = gen.generate(model, tokenizer, prompt, length)
    await ctx.send(response)

bot.run('')