import logging
import tabulate
from pyfiglet import figlet_format
import discord
import json

class Trial:
	left_name = ''
	right_name = ''
	name = ''
	standings = {}
	status_message = None
	def __init__(self, left, right):
		self.id = 0
		self.left_name = left.capitalize()
		self.right_name = right.capitalize()
		self.name = '%s v. %s' % (left.title(), right.title())
		self.standings['left'] = []
		self.standings['fence'] = []
		self.standings['right'] = []
		logging.info('Creating new argument (%s): %s v. %s' % (self.id, self.left_name, self.right_name))

	def __str__(self):
		return self.name

	def vote(self, team, username):
		if team not in self.standings:
			return 1
		elif username in self.standings[team]:
			return 0
		else:
			if username in self.standings['left']:
				self.standings['left'].remove(username)
			if username in self.standings['fence']:
				self.standings['fence'].remove(username)
			if username in self.standings['right']:
				self.standings['right'].remove(username)
			self.standings[team].append(username)
			return 0

	def status(self):
		logging.info(self.standings)
		embed = discord.Embed()
		embed.title = '%s v. %s' % (self.left_name, self.right_name)
		# embed.description = '```%s```' % tabulate.tabulate(self.standings, headers = [self.left_name, 'The Fence', self.right_name], tablefmt='grid')
		print('\n'.join(self.standings['left']))
		if self.standings['left']:
			value = '\n'.join(self.standings['left'])
		else:
			value = '‌‌ '
		embed.add_field(name="__" + self.left_name + "__", value=value)
		if self.standings['fence']:
			value = '\n'.join(self.standings['fence'])
		else:
			value = '‌‌ '
		embed.add_field(name="__The Fence__", value=value)
		if self.standings['right']:
			value = '\n'.join(self.standings['right'])
		else:
			value = '‌‌ '
		embed.add_field(name="__" + self.right_name + "__", value=value)
		return embed

	def toJSON(self):
		output = {
			"name": self.name,
			"id": self.id,
			"left_name": self.left_name,
			"right_name": self.right_name,
			"standings": self.standings
		}
		return json.dumps(output)