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
	votes = {}
	status_message = None
	def __init__(self, left, right):
		self.id = 0
		self.left_name = left.capitalize()
		self.right_name = right.capitalize()
		self.name = '%s v. %s' % (left.title(), right.title())
		self.description = ""
		self.votes[self.left_name.lower()] = []
		self.votes['fence'] = []
		self.votes[self.right_name.lower()] = []
		self.standings['left'] = []
		self.standings['fence'] = []
		self.standings['right'] = []
		logging.info('Creating new argument (%s): %s v. %s' % (self.id, self.left_name, self.right_name))

	def __str__(self):
		return self.name

	def vote(self, team, username):
		team = team.lower()
		if team not in self.votes:
			return 1
		elif username in self.votes[team]:
			return 0
		else:
			for current_team in self.votes.keys():
				if username in self.votes[current_team]:
					self.votes[current_team].remove(username)
			self.votes[team].append(username)
			return 0

	def status(self):
		output = {}
		title = ""
		for item in self.votes.keys():
			if item != "fence":
				title = title + "%s v. " % item.title()
		if title.endswith(" v. "):
			title = title[:-4]
		output['title'] = title
		output['description'] = self.description
		output['votes'] = self.votes
		return output
		# logging.info(self.standings)
		# embed = discord.Embed()
		# embed.title = '%s v. %s' % (self.left_name, self.right_name)
		# # embed.description = '```%s```' % tabulate.tabulate(self.standings, headers = [self.left_name, 'The Fence', self.right_name], tablefmt='grid')
		# print('\n'.join(self.standings['left']))
		# if self.standings['left']:
		# 	value = '\n'.join(self.standings['left'])
		# else:
		# 	value = '‌‌ '
		# embed.add_field(name="__" + self.left_name + "__", value=value)
		# if self.standings['fence']:
		# 	value = '\n'.join(self.standings['fence'])
		# else:
		# 	value = '‌‌ '
		# embed.add_field(name="__The Fence__", value=value)
		# if self.standings['right']:
		# 	value = '\n'.join(self.standings['right'])
		# else:
		# 	value = '‌‌ '
		# embed.add_field(name="__" + self.right_name + "__", value=value)
		# return embed

	def toJSON(self):
		output = {
			"name": self.name,
			"id": self.id,
			"left_name": self.left_name,
			"right_name": self.right_name,
			"standings": self.standings
		}
		return json.dumps(output)