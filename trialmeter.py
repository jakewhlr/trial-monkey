#!/usr/bin/env python3
import discord
from discord.ext import commands
import uuid
import tabulate
from pyfiglet import figlet_format
import re

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

bot = commands.Bot(command_prefix='!')
arguments = []

@bot.command()
async def new_trial(ctx, left, right):
	left_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', left)
	right_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', right)
	arguments.append(argument(left_split, right_split))
	await ctx.send('```' + 
					figlet_format(arguments[-1].left_name, font='starwars') + 
					figlet_format('versus', font='slant') + 
					figlet_format(arguments[-1].right_name, font='starwars') + 
				   '```')
	status_message = await ctx.send('```' + arguments[-1].status() + '```')
	await status_message.add_reaction('👈')
	await status_message.add_reaction('🤺')
	await status_message.add_reaction('👉')

@bot.command()
async def status(ctx):
	await ctx.send('```' + 
					figlet_format(arguments[-1].left_name, font='starwars') + 
					figlet_format('versus', font='slant') + 
					figlet_format(arguments[-1].right_name, font='starwars') + 
				   '```')
	status_message = await ctx.send('```' + arguments[-1].status() + '```')
	await status_message.add_reaction('👈')
	await status_message.add_reaction('🤺')
	await status_message.add_reaction('👉')

bot.run('NTg0MTIzNTE0MDMwNzg0NTIz.XPGWGw.d13Vnanchf_QMYJmfjq-uAw9Q0M')
