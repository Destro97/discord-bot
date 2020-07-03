import json
import os


from discord.ext.commands import Bot


from database import DB
from google_search import fetch_search_results


### Load Discord Token from environment on PROD
### Otherwise load it from local file
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    env_config = json.loads(open('dev.json', 'r').read())
    DISCORD_TOKEN = env_config.get('DISCORD_TOKEN')


### Initialise Discord BOT API Client
bot = Bot(command_prefix='!')


### Specify commands
@bot.command(name='hi', help='Responds with Greeting')
async def greet(ctx):

    await ctx.send(f"Hey {ctx.message.author.display_name}")


@bot.command(name='google', help='Responds with top 5 results of Google Search with specified search term(s)')
async def googlesearch(ctx, *terms):

    ### Combines multiple search terms into space separated string
    search_term = " ".join(list(terms)).strip()

    ### Check if there was no search term(s) provided
    if not search_term:
        await ctx.send("Usage: !google <search-term(s)>")
    else:

        ### Connect to DB
        db_instance = DB()

        ### Dict of data to be stored in DB as search history entry
        ### containing basic information associated with the request
        search_request_data = {
            'guild': ctx.guild.name,
            'guild_id': ctx.guild.id,
            'channel': ctx.channel.name,
            'author': ctx.message.author.display_name,
            'term': search_term
        }

        ### Store the data inside MongoDB
        db_instance.store(**search_request_data)

        ### Search google for the provided search term(s)
        search_results = fetch_search_results(search_term)

        ### Check if any fetching results from successful or not
        if search_results.get('success', False):
            ### Combine the search results into new line separated strings
            response_links = '\n'.join([_ for _ in search_results.get('results', [])])

            ### Return response with search results
            await ctx.send(f"Top Results from Google for '{search_term}' are:\n{response_links}")
        else:
            ### Return response in case of failure in searching
            await ctx.send(f"Error while fetching search results from Google for {search_term}")


@bot.command(name='recent', help='Returns recent search terms matching the provided term')
async def recents(ctx, term=None):

    ### Check if there was no search term provided
    if term is None:

        ### Return response in case no search term was provided
        await ctx.send("Usage: !recent <term>")
    else:

        ### Connect to DB
        db_instance = DB()

        ### Fetch Guild ID to only query search history of that Guild
        guild_id = ctx.guild.id

        ### Fetch previous search results for particular Guild matching with provided search term
        search_result = db_instance.search_term(term=term, guild_id=guild_id)

        ### Check if any fetching results from successful or not
        if search_result.get('success', False):
            if search_result.get('results', []):
                ### Combine search results into new line separated strings
                results = '\n'.join([result.get('term', '') for result in search_result.get('results', [])])

                ### Return response with search results
                await ctx.send(f"Recent Similar searches to '{term}' are:\n{results}")
            else:
                ### Return response in case no results matching provided input were found
                await ctx.send(f"No recent searches match the provided term {term}")
        else:
            ### Return response in case of failure in searching
            await ctx.send(f"Error while fetching querying search history for {term}")


bot.run(DISCORD_TOKEN)
