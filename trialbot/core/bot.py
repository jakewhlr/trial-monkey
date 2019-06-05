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

class argument:
	left_name = ''
	right_name = ''
	name = ''
	left = []
	right = []
	fence = []
	standings = []
	def __init__(self, left, right):
		self.id = str(uuid.uuid4())
		self.left_name = left
		self.right_name = right
		self.name = '%s v. %s' % (left.title(), right.title())
		print('creating argument:', self.left_name, self.right_name, self.id)

	def __str__(self):
		return self.name

	def status(self):
		self.standings = [self.left, self.fence, self.right]
		rotated90 = zip(*self.standings[::-1])
		outstring = tabulate.tabulate(rotated90, headers = [self.left_name, 'The Fence', self.right_name], tablefmt='grid')
		return outstring

class TrialBot:
	__version__ = '0.0.1'

	client = discord.Client()
	bot = commands.Bot(command_prefix='!')
	arguments = []
	token = None

	def __init__(self, token):
		self.token = token
		try:
			print('Starting bot...')
		except:
			pass

	async def start(self):
		print("running bot")
		await self.bot.start(self.token)

	def stop(self):
		self.bot.close()


	@bot.event
	async def on_message(message):
		def check(reaction, user):
			return user == message.author and str(reaction.emoji)

		async def vote():
			if message.content.startswith('```\n+-------+-------------+-------+'):
				channel = message.channel
				current_arg = TrialBot.arguments[-1]
				try:
					reaction, user = await TrialBot.bot.wait_for('reaction_add', timeout=15.0, check=check)
				except asyncio.TimeoutError:
					print('Stopping...')
				else:
					# await channel.send(str(reaction) + ' ' + str(user))
					if str(reaction) == '👈':
						print(reaction)
						if user in current_arg.left:
							print(user, "in left")
							filter(lambda a: a != user, current_arg.left)
						current_arg.left.append(user)
					if str(reaction) == '🤺':
						print(reaction)
						if str(user) in current_arg.fence:
							print(user, "on fence")
							filter(lambda a: a != user, current_arg.fence)
						current_arg.fence.append(user)
					if str(reaction) == '👉':
						print(reaction)
						if user in current_arg.right:
							print(right, 'in right')
							filter(lambda a: a != user, current_arg.right)
						current_arg.right.append(user)
						
					print(TrialBot.arguments[-1].status())
					await vote()
		await vote()
		await TrialBot.bot.process_commands(message)

	@bot.command()
	async def new_trial(ctx, left, right):
		gifs = [line.rstrip('\n') for line in open('gifs.txt')]
		monkey_gif = random.choice(gifs)
		left_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', left)
		right_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', right)
		TrialBot.arguments.append(argument(left_split, right_split))
		current_arg = TrialBot.arguments[-1]
		left_display = '```\n%s\n```' % figlet_format(current_arg.left_name, font='starwars')
		versus_display = '```\n%s\n```' % figlet_format('versus', font='slant')
		right_display = '```\n%s\n```' % figlet_format(current_arg.right_name, font='starwars')
		status_display = '```\n%s\n```' % current_arg.status()
		await ctx.send(monkey_gif)
		sleep(random.randint(3,10))
		print(left_display)
		await ctx.send(left_display)
		print(versus_display)
		await ctx.send(versus_display)
		print(right_display)
		await ctx.send(right_display)
		print(status_display)
		print(monkey_gif)
		status_message = await ctx.send(status_display)
		await status_message.add_reaction('👈')
		await status_message.add_reaction('🤺')
		await status_message.add_reaction('👉')

	@bot.command()
	async def status(ctx):
		current_arg = TrialBot.arguments[-1]
		left_display = '```\n%s\n```' % figlet_format(current_arg.left_name, font='starwars')
		versus_display = '```\n%s\n```' % figlet_format('versus', font='slant')
		right_display = '```\n%s\n```' % figlet_format(current_arg.right_name, font='starwars')
		status_display = '```\n%s\n```' % current_arg.status()
		print(left_display)
		await ctx.send(left_display)
		print(versus_display)
		await ctx.send(versus_display)
		print(right_display)
		await ctx.send(right_display)
		print(status_display)
		status_message = await ctx.send(status_display)
		await status_message.add_reaction('👈')
		await status_message.add_reaction('🤺')
		await status_message.add_reaction('👉')
