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

	def status(self):
		logging.info(self.standings)
		embed = {}
		embed['title'] = '%s v. %s' % (self.left_name, self.right_name)
		embed['description'] = '```%s```' % tabulate.tabulate(self.standings, headers = [self.left_name, 'The Fence', self.right_name], tablefmt='grid')
		return discord.Embed.from_dict(embed)

	def toJSON(self):
		output = {
			"name": self.name,
			"id": self.id,
			"left_name": self.left_name,
			"right_name": self.right_name,
			"standings": self.standings
		}
		return json.dumps(output)