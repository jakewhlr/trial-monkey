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
from core.trial import Trial

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')
logging.basicConfig(format = '%(levelname)s: %(message)s', level = logging.INFO)

class TrialBot:
	__version__ = '0.0.1'

	client = discord.Client()
	bot = commands.Bot(command_prefix='!', case_insensitive=True)
	current_arg = None
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
		TrialBot.bot.command_prefix = "<@%s> " % TrialBot.bot.user.id
		logging.info("Set command prefix to: %s" % TrialBot.bot.command_prefix)

	@bot.event
	async def on_reaction_add(reaction, user):
		try:
			if TrialBot.current_arg.status_message.id == reaction.message.id:
				if user.id != reaction.message.author.id:
					for key in TrialBot.current_arg.standings:
						if user.name in TrialBot.current_arg.standings[key]:
							TrialBot.current_arg.standings[key].remove(user.name)
					if str(reaction) == '👈':
						TrialBot.current_arg.standings['left'].append(user.name)
					elif str(reaction) == '🤺':
						TrialBot.current_arg.standings['fence'].append(user.name)
					elif str(reaction) == '👉':
						TrialBot.current_arg.standings['right'].append(user.name)
					await reaction.remove(user)
					await TrialBot.current_arg.status_message.edit(embed=TrialBot.current_arg.status())
		except Exception as e:
			logging.error(e)
			return

	@bot.command(help="Sends mokney gif")
	async def gif(ctx):
		gifs = [line.rstrip('\n') for line in open(os.path.join(BASE_DIR, 'gifs.txt'))]
		monkey_gif = random.choice(gifs)
		await ctx.send(monkey_gif)

	@bot.command(pass_context=True, help="Creates new trial", usage="(<plaintiff> <defendant>)")
	async def new(ctx, left, right):
		gif = await TrialBot.gif.invoke(ctx)
		sleep(random.randint(3,10))
		left_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', left)
		right_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', right)
		TrialBot.current_arg = Trial(left_split, right_split)
		# left_display = '```\n%s\n```' % figlet_format(current_arg.left_name, font='starwars')
		# versus_display = '```\n%s\n```' % figlet_format('versus', font='slant')
		# right_display = '```\n%s\n```' % figlet_format(current_arg.right_name, font='starwars')

		# await ctx.send(left_display)
		# await ctx.send(versus_display)
		# await ctx.send(right_display)
		TrialBot.current_arg.status_message = await ctx.send(embed = TrialBot.current_arg.status())
		await TrialBot.current_arg.status_message.add_reaction('👈')
		sleep(0.5)
		await TrialBot.current_arg.status_message.add_reaction('🤺')
		sleep(0.5)
		await TrialBot.current_arg.status_message.add_reaction('👉')

	@bot.command(help="Shows status of given trial (default=current)", usage="[<trial_number>]")
	async def status(ctx):
		try:
			await TrialBot.current_arg.status_message.delete()
			TrialBot.current_arg.status_message = await ctx.send(embed = TrialBot.current_arg.status())
			await TrialBot.current_arg.status_message.add_reaction('👈')
			sleep(0.5)
			await TrialBot.current_arg.status_message.add_reaction('🤺')
			sleep(0.5)
			await TrialBot.current_arg.status_message.add_reaction('👉')
		except:
			await ctx.send("No trials available!")

	@bot.command()
	async def adjourn(ctx):
		await ctx.send('COURT ADJOURNED')
		left_total = len(TrialBot.current_arg.standings['left'])
		right_total = len(TrialBot.current_arg.standings['right'])
		if left_total == right_total:
			await ctx.send("It's a tie!")
			await ctx.send("You both suck")
		elif left_total > right_total:
			await ctx.send("%s wins with %d votes!" % (TrialBot.current_arg.left_name, left_total))
			await ctx.send("Suck it %s" % TrialBot.current_arg.right_name)
		elif right_total > left_total:
			await ctx.send("%s wins with %d votes!" % (TrialBot.current_arg.right_name, right_total))
			await ctx.send("Suck it %s" % TrialBot.current_arg.left_name)

	@bot.command()
	async def boomer(ctx):
		await ctx.send('https://imgur.com/0RGV10v')
