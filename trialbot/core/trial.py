import logging
import tabulate
from pyfiglet import figlet_format
import uuid
import discord

class Trial:
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