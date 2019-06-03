#!/usr/bin/env python3
import discord
from discord.ext import commands
import uuid
import tabulate
from pyfiglet import figlet_format
import re
import json

class argument:
	left_name = ''
	right_name = ''
	name = ''
	def __init__(self, left, right):
		self.id = str(uuid.uuid4())
		self.left_name = left
		self.right_name = right
		self.name = '%s v. %s' % (left.title(), right.title())
		print('creating argument:', self.left_name, self.right_name, self.id)

	def __str__(self):
		return self.name

	def status(self):
		outstring = tabulate.tabulate([[], [], []], headers = [self.left_name, 'The Fence', self.right_name], tablefmt='grid')
		return outstring

class trialbot:
	bot = commands.Bot(command_prefix='!')
	# arguments = []
	token = None

	def __init__(self, token):
		self.token = token

	def start(self):
		self.bot.run(self.token)

	@bot.command()
	async def new_trial(ctx, left, right):
		left_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', left)
		right_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', right)
		current_arg = argument(left_split, right_split)
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


	@bot.command()
	async def status(ctx):
		left_display = '```\n%s\n```' % figlet_format(arguments[-1].left_name, font='starwars')
		versus_display = '```\n%s\n```' % figlet_format('versus', font='slant')
		right_display = '```\n%s\n```' % figlet_format(arguments[-1].right_name, font='starwars')
		status_display = '```\n%s\n```' % arguments[-1].status()
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
