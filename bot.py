import json
import os


from discord.ext.commands import Bot


from database import DB
from google_search import fetch_search_results


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    env_config = json.loads(open('dev.json', 'r').read())
    DISCORD_TOKEN = env_config.get('DISCORD_TOKEN')


bot = Bot(command_prefix='!')


@bot.command(name='hi', help='Responds with Greeting')
async def greet(ctx):
    await ctx.send(f"Hey {ctx.message.author.display_name}")


@bot.command(name='google', help='Responds with top 5 results of Google Search with specified search term(s)')
async def googlesearch(ctx, *terms):
    search_term = " ".join(list(terms)).strip()
    if not search_term:
        await ctx.send("Usage: !google <search-term(s)>")
    else:
        db_instance = DB()
        search_request_data = {
            'guild': ctx.guild.name,
            'guild_id': ctx.guild.id,
            'channel': ctx.channel.name,
            'author': ctx.message.author.display_name,
            'term': search_term
        }
        db_instance.store(**search_request_data)
        search_results = fetch_search_results(search_term)
        if search_results.get('success', False):
            response_links = '\n'.join([_ for _ in search_results.get('results', [])])
            await ctx.send(f"Top Results from Google for '{search_term}' are:\n{response_links}")
        else:
            await ctx.send(f"Error while fetching search results from Google for {search_term}")


@bot.command(name='recent', help='Returns recent search terms matching the provided term')
async def recents(ctx, term=None):
    if term is None:
        await ctx.send("Usage: !recent <term>")
    else:
        db_instance = DB()
        guild_id = ctx.guild.id
        search_result = db_instance.search_term(term=term, guild_id=guild_id)
        if search_result.get('success', False):
            if search_result.get('results', []):
                results = '\n'.join([result.get('term', '') for result in search_result.get('results', [])])
                await ctx.send(f"Recent Similar searches to '{term}' are:\n{results}")
            else:
                await ctx.send(f"No recent searches match the provided term {term}")
        else:
            await ctx.send(f"Error while fetching querying search history for {term}")


bot.run(DISCORD_TOKEN)
