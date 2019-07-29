#!/usr/bin/env python3
import discord
from discord.ext import commands
import uuid
import tabulate
from pyfiglet import figlet_format
import re
import json
import asyncio
import random
from time import sleep
import logging
import os

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')
logging.basicConfig(format = '%(levelname)s: %(message)s', level = logging.INFO)

class argument:
	left_name = ''
	right_name = ''
	name = ''
	standings = {}
	left = []
	right = []
	fence = []
	status_message = None
	def __init__(self, left, right):
		self.id = str(uuid.uuid4())
		self.left_name = left.capitalize()
		self.right_name = right.capitalize()
		self.name = '%s v. %s' % (left.title(), right.title())
		self.standings['left'] = []
		self.standings['fence'] = []
		self.standings['right'] = []
		logging.info('Creating new argument (%s): %s v. %s' % (self.id, self.left_name, self.right_name))

	def __str__(self):
		return self.name

	def status(self):
		logging.info(self.left)
		logging.info(self.fence)
		logging.info(self.right)
		logging.info(self.standings)
		embed = {}
		embed['title'] = '%s v. %s' % (self.left_name, self.right_name)
		embed['description'] = '```%s```' % tabulate.tabulate(self.standings, headers = [self.left_name, 'The Fence', self.right_name], tablefmt='grid')
		return discord.Embed.from_dict(embed)

class TrialBot:
	__version__ = '0.0.1'

	client = discord.Client()
	bot = commands.Bot(command_prefix='!')
	arguments = []
	token = None

	def __init__(self, token):
		self.token = token

	async def start(self):
		await self.bot.login(self.token, bot=True)
		await self.bot.connect()

	async def stop(self):
		logging.info("logging out")
		await self.bot.close()

	@bot.event
	async def on_ready():
		logging.info("Connected as %s" % TrialBot.bot.user)
		TrialBot.bot.command_prefix = "<@%s> !" % TrialBot.bot.user.id
		logging.info("Set command prefix to: %s" % TrialBot.bot.command_prefix)

	@bot.event
	async def on_reaction_add(reaction, user):
		current_arg = TrialBot.arguments[-1]
		try:
			if current_arg.status_message.id == reaction.message.id:
				if user.id != reaction.message.author.id:
					for key in current_arg.standings:
						if user.name in current_arg.standings[key]:
							current_arg.standings[key].remove(user.name)
					if str(reaction) == '👈':
						current_arg.standings['left'].append(user.name)
					elif str(reaction) == '🤺':
						current_arg.standings['fence'].append(user.name)
					elif str(reaction) == '👉':
						current_arg.standings['right'].append(user.name)
					await reaction.remove(user)
					await current_arg.status_message.edit(embed=current_arg.status())
		except Exception as e:
			logging.error(e)
			return

	@bot.command(help="Sends mokney gif")
	async def gif(ctx):
		gifs = [line.rstrip('\n') for line in open(os.path.join(BASE_DIR, 'gifs.txt'))]
		monkey_gif = random.choice(gifs)
		await ctx.send(monkey_gif)
		sleep(random.randint(3,10))

	@bot.command(pass_context=True, help="Creates new trial", usage="(<plaintiff> <defendant>)")
	async def new(ctx, left, right):
		await TrialBot.gif.invoke(ctx)

		left_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', left)
		right_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', right)
		TrialBot.arguments.append(argument(left_split, right_split))
		current_arg = TrialBot.arguments[-1]
		left_display = '```\n%s\n```' % figlet_format(current_arg.left_name, font='starwars')
		versus_display = '```\n%s\n```' % figlet_format('versus', font='slant')
		right_display = '```\n%s\n```' % figlet_format(current_arg.right_name, font='starwars')

		await ctx.send(left_display)
		await ctx.send(versus_display)
		await ctx.send(right_display)
		current_arg.status_message = await ctx.send(embed = current_arg.status())
		await current_arg.status_message.add_reaction('👈')
		sleep(0.5)
		await current_arg.status_message.add_reaction('🤺')
		sleep(0.5)
		await current_arg.status_message.add_reaction('👉')

	@bot.command(help="Shows status of given trial (default=current)", usage="[<trial_number>]")
	async def status(ctx):
		try:
			current_arg = TrialBot.arguments[-1]
			await current_arg.status_message.delete()
			current_arg.status_message = await ctx.send(embed = current_arg.status())
			await current_arg.status_message.add_reaction('👈')
			sleep(0.5)
			await current_arg.status_message.add_reaction('🤺')
			sleep(0.5)
			await current_arg.status_message.add_reaction('👉')
		except:
			await ctx.send("No trials available!")

	@bot.command()
	async def adjourn(ctx):
		await ctx.send('COURT ADJOURNED')
