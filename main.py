import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
import keep_alive as alive
import helpers

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
PREFIX = os.getenv("DEFAULT_PREFIX")

# bot initiate + access to mongodb
client = MongoClient(
    "MongoDB CLuster connect link here"
)
# access collection
quote_db = client['jojo-quotes']['quotes']
prefix_db = client['jojo-quotes']['server-prefix']


async def determine_prefix(bot, message):
	guild = message.guild
    # Only allow custom prefixes in guild
	if guild:
		custom_prefix = prefix_db.find_one({"guild_id": guild.id})
		if not custom_prefix:
			return PREFIX
		return custom_prefix['prefix']
	else:
		return PREFIX

bot = commands.Bot(command_prefix=determine_prefix)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# command !q -> output a random quote
@bot.command(name='q')
async def quote(ctx, *args):
	option_pool = list()
	if not args:
		option_pool.extend(list(quote_db.find()))
	else:
		for arg in args:
			if helpers.int_in_disguise(arg):
				option_pool.extend(list(quote_db.find({"part": int(arg)})))
	if not option_pool:
		await ctx.send(
		f'Sorry, I can\'t find any quotes that fit your criteria.'
		)
		return
	
	# message generator
	chosen_quote = random.choice(option_pool)
	content = chosen_quote['content']
	user = chosen_quote['user']
	chapter = chosen_quote['chapter']
	part = chosen_quote['part']
	await ctx.send(
		f'> {content}\n\n*{user} - chapter {chapter}, part {part}*'
	)


# !prefix [new-prefix] to change prefix for the server
@bot.command(name='prefix', help='change prefix')
@commands.guild_only()
async def set_prefix(ctx, *prefix):
	id = ctx.guild.id
	if not prefix:
		await ctx.send("""
Please add an additional argument. For example: 
> !prefix ?   
to change the prefix to ?
		""")
	else:
		current_prefix = prefix_db.find_one({"guild_id":id})
		if current_prefix:
			prefix_db.update_one(
				{"guild_id":id},
				{"$set":{
					"prefix" : prefix
				}}
				)
		else:
			new_entry = {
				"guild_id" : id,
				"prefix" : prefix
			}
			prefix_db.insert_one(new_entry)
		await ctx.send("Prefix changed!")
		


@bot.command(name='ping')
async def ping_pong(ctx):
    await ctx.send('pong!')


# keep the server alive 24/7
alive.keep_alive()
bot.run(TOKEN)
