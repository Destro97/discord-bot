import os
import json


from discord.ext.commands import Bot


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    env_config = json.loads(open('dev.json', 'r').read())
    DISCORD_TOKEN = env_config.get('DISCORD_TOKEN')


bot = Bot(command_prefix='!')


@bot.command(name='hi', help='Responds with a random quote from Brooklyn 99')
async def greet(ctx):
    await ctx.send(f"Hey {ctx.message.author.display_name}")


bot.run(DISCORD_TOKEN)
