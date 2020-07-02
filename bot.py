import os
import json


from discord.ext.commands import Bot


from google_search import fetch_search_results


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    env_config = json.loads(open('dev.json', 'r').read())
    DISCORD_TOKEN = env_config.get('DISCORD_TOKEN')


bot = Bot(command_prefix='!')


@bot.command(name='hi', help='Responds with a random quote from Brooklyn 99')
async def greet(ctx):
    await ctx.send(f"Hey {ctx.message.author.display_name}")


@bot.command(name='google', help='Responds with top 5 results of Google Search with specified search term')
async def googlesearch(ctx, term=None):
    if term is None:
        await ctx.send("Usage: !google <search-term>")
    else:
        search_results = fetch_search_results(term)
        if search_results.get('success', False):
            response_links = '\n'.join([link for link in search_results.get('results', [])])
            await ctx.send(f"Top Results from Google for '{term}' are:\n{response_links}")
        else:
            await ctx.send(f"Error while fetching search results from Google for {term}")


bot.run(DISCORD_TOKEN)
