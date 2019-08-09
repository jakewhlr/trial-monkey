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
import sqlite3
from .trial import Trial

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')
logging.basicConfig(format = '%(levelname)s: %(message)s', level = logging.INFO)

EMOJI = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']

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
		self.sqlite_conn = self.create_db_connection(os.path.join(BASE_DIR, 'db.sqlite3'))
		self.initialize_db(self.sqlite_conn)
		self.sqlite_conn.close()

	async def start(self):
		await self.bot.login(self.token, bot=True)
		await self.bot.connect()

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

	def set_command_prefix(self, new_command_prefix):
		if new_command_prefix:
			try:
				self.bot.command_prefix = new_command_prefix
				return 0
			except Exception as e:
				logging.error(e)
		else:
			return 1

	def check_valid_reaction(self, bot_user_id, status_message_id, message_id, user_id, emoji):
		if message_id != status_message_id:
			logging.info("Failed at message id")
			logging.info(message_id)
			logging.info(status_message_id)
			return False
		elif user_id == bot_user_id:
			logging.info("Failed at user id")
			return False
		elif emoji not in self.assigned_emoji.keys():
			logging.info("Failed at emoji")
			logging.info(str(self.assigned_emoji.keys()))
			return False
		else:
			return True

	def split_args(self, args_string):
		split_options = re.split(' v | v. | vs | vs. | versus ', args_string)
		if len(split_options) < 2:
			return None
		else:
			return split_options

	def create_db_connection(self, db_file):
		try:
			conn = sqlite3.connect(db_file)
			return conn
		except Exception as e:
			logging.error(e)
		return None

	def initialize_db(self, conn):
		try:
			cursor = conn.cursor()
			logging.info("Executing SQL create trials")
			cursor.execute(
				"""
					CREATE TABLE IF NOT EXISTS trials(
						title text PRIMARY KEY,
						description text
					);
				"""
			)
			logging.info("Executing SQL create teams")
			cursor.execute(
				"""
					CREATE TABLE IF NOT EXISTS teams(
						team_name text PRIMARY KEY,
						trial_title integer,
						FOREIGN KEY (trial_title) REFERENCES trials (title)
					);
				"""
			)
			logging.info("Executing SQL create trials")
			cursor.execute(
				"""
					CREATE TABLE IF NOT EXISTS votes(
						user_name text PRIMARY KEY,
						team_name integer,
						trial_title text,
						FOREIGN KEY (team_name) REFERENCES teams(team_name),
						FOREIGH KEY (trial_title) REFERENCES trials(title)
					);
				"""
			)
		except Exception as e:
			logging.error(e)
		return

	def save_to_db(self, conn):
		'''
			Saves current trial to sqlite database
		'''
		cursor = conn.cursor()
		status_dict = self.current_arg.status()
		cursor.execute(
			"""
				INSERT OR REPLACE INTO trials(title, description)
				VALUES (?, ?)
			""", (status_dict['title'], status_dict['description'])
		)
		for team in status_dict['votes'].keys():
			print(team)
			cursor.execute(
				"""
					INSERT OR REPLACE INTO teams(team_name)
					VALUES (?)
				""", (team,)
			)
			execute_list = []
			for item in status_dict['votes'][team]:
				execute_list.append([item, team, status_dict['title']])
			logging.info("EXECUTE LIST" + str(execute_list))
			cursor.executemany(
				"""
					INSERT OR REPLACE INTO votes(user_name, team_name, trial_name)
					VALUES (?, ?, ?)
				""", execute_list
			)
		conn.commit()

	@bot.event
	async def on_ready():
		TrialBot.set_command_prefix(TrialBot, "<@%s> " % TrialBot.bot.user.id)

	@bot.event
	async def on_reaction_add(reaction, user):
		is_valid_reaction = TrialBot.check_valid_reaction(TrialBot,
			bot_user_id = user.id,
			status_message_id = TrialBot.current_arg.status_message.id,
			message_id = reaction.message.id,
			user_id = reaction.message.author.id,
			emoji = str(reaction)
		)
		if is_valid_reaction:
			try:
				TrialBot.current_arg.vote(TrialBot.assigned_emoji[str(reaction)], user.name)
				await reaction.remove(user)
				await TrialBot.current_arg.status_message.edit(embed=TrialBot.gen_status_embed(TrialBot, TrialBot.current_arg))
				return 0
			except Exception as e:
				logging.error(e)
				return 1
		else:
			return 1

	@bot.command(help="Sends mokney gif")
	async def gif(ctx):
		gifs = [line.rstrip('\n') for line in open(os.path.join(BASE_DIR, 'gifs.txt'))]
		monkey_gif = random.choice(gifs)
		await ctx.send(monkey_gif)

	@bot.command(pass_context=True, help="Creates new trial", usage="(<plaintiff> <defendant>)")
	async def new(ctx, *, arg):
		args_list = TrialBot.split_args(TrialBot, arg)
		if not args_list:
			return 0
		await TrialBot.gif.invoke(ctx)
		sleep(random.randint(3,10))
		if TrialBot.current_arg:
			TrialBot.current_arg.votes = {}
		TrialBot.current_arg = Trial(args_list)
		TrialBot.assigned_emoji = dict(zip(EMOJI, TrialBot.current_arg.votes.keys()))
		TrialBot.assigned_emoji_inv = {v: k for k, v in TrialBot.assigned_emoji.items()}
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

	@bot.command()
	async def save(ctx):
		conn = TrialBot.create_db_connection(TrialBot, os.path.join(BASE_DIR, 'db.sqlite3'))
		TrialBot.save_to_db(TrialBot, conn)
		conn.close()

