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

EMOJI = ['1⃣', '2⃣', '3⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

class TrialBot:
	__version__ = '0.0.1'

	client = discord.Client()
	bot = commands.Bot(command_prefix='!', case_insensitive=True)
	current_arg = None
	token = None
	assigned_emoji = {}
	assigned_emoji_inv = {}

	def __init__(self, token):
		self.token = token

	async def start(self):
		await self.bot.login(self.token, bot=True)
		await self.bot.connect()

	async def stop(self):
		logging.info("logging out")
		await self.bot.close()

	def gen_status_embed(self, trial):
		status_dict = trial.status()
		status_embed = discord.Embed()
		status_embed.title = status_dict['title']
		status_embed.description = status_dict['description']
		for item in status_dict['votes'].keys():
			name = self.assigned_emoji_inv[item] + " " + item.title()
			if status_dict['votes'][item]:
				value = '\n'.join(status_dict['votes'][item])
			else:
				value = '‌‌ '
			status_embed.add_field(name=name, value=value)
		return status_embed

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
					try:
						TrialBot.current_arg.vote(TrialBot.assigned_emoji[str(reaction)], user.name)
					except Exception as e:
						logging.error(e)
					await reaction.remove(user)
					await TrialBot.current_arg.status_message.edit(embed=TrialBot.gen_status_embed(TrialBot, TrialBot.current_arg))
			return 0
		except Exception as e:
		logging.error(e)
		return 1

	@bot.command(help="Sends mokney gif")
	async def gif(ctx):
		gifs = [line.rstrip('\n') for line in open(os.path.join(BASE_DIR, 'gifs.txt'))]
		monkey_gif = random.choice(gifs)
		await ctx.send(monkey_gif)

	@bot.command(pass_context=True, help="Creates new trial", usage="(<plaintiff> <defendant>)")
	async def new(ctx, left, right):
		left_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', left)
		right_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', right)
		TrialBot.current_arg = Trial(left_split, right_split)
		TrialBot.assigned_emoji = dict(zip(EMOJI, TrialBot.current_arg.votes.keys()))
		TrialBot.assigned_emoji_inv = {v: k for k, v in TrialBot.assigned_emoji.items()}
		await TrialBot.gif.invoke(ctx)
		sleep(random.randint(3,10))
		await TrialBot.status.invoke(ctx)

	@bot.command(help="Shows status of given trial (default=current)", usage="[<trial_number>]")
	async def status(ctx):
		try:
			if TrialBot.current_arg.status_message:
				await TrialBot.current_arg.status_message.delete()
			TrialBot.current_arg.status_message = await ctx.send(embed=TrialBot.gen_status_embed(TrialBot, TrialBot.current_arg))
			for emoji in TrialBot.assigned_emoji:
				await TrialBot.current_arg.status_message.add_reaction(emoji)
				sleep(0.5)
		except Exception as e:
			logging.error(e)

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
